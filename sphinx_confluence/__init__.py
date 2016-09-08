# -*- coding: utf-8 -*-
"""

https://confluence.atlassian.com/display/DOC/Confluence+Storage+Format

"""

import os

from docutils import nodes
from docutils.parsers.rst import directives, Directive, roles
from docutils.parsers.rst.directives import images
from docutils.parsers.rst.roles import set_classes
from sphinx.builders.html import JSONHTMLBuilder
from sphinx.locale import _
from sphinx.writers.html import HTMLTranslator


def true_false(argument):
    return directives.choice(argument, ('true', 'false'))


def static_dynamic(argument):
    return directives.choice(argument, ('static', 'dynamic'))


class TitlesCache(object):
    titles = {}

    @staticmethod
    def _document_key(document):
        return hash(document)

    @classmethod
    def set_title(cls, document, title):
        cls.titles[cls._document_key(document)] = title

    @classmethod
    def get_title(cls, document):
        return cls.titles.get(cls._document_key(document), None)

    @classmethod
    def has_title(cls, document):
        return cls._document_key(document) in cls.titles


class JSONConfluenceBuilder(JSONHTMLBuilder):
    """For backward compatibility"""

    name = 'json_conf'

    def __init__(self, app):
        super(JSONConfluenceBuilder, self).__init__(app)
        self.warn('json_conf builder is deprecated and will be removed in future releases')


class HTMLConfluenceTranslator(HTMLTranslator):
    def unimplemented_visit(self, node):
        self.builder.warn('Unimplemented visit is not implemented for node: {}'.format(node))

    def unknown_visit(self, node):
        self.builder.warn('Unknown visit is not implemented for node: {}'.format(node))

    def visit_admonition(self, node, name=''):
        """
        Info, Tip, Note, and Warning Macros

        https://confluence.atlassian.com/conf58/info-tip-note-and-warning-macros-771892344.html

        <ac:structured-macro ac:name="info">
          <ac:parameter ac:name="icon">false</ac:parameter>
          <ac:parameter ac:name="title">This is my title</ac:parameter>
          <ac:rich-text-body>
            <p>
              This is important information.
            </p>
          </ac:rich-text-body>
        </ac:structured-macro>
        """

        confluence_admonition_map = {
            'note': 'info',
            'warning': 'note',
            'attention': 'note',
            'hint': 'tip',
            'tip': 'tip',
            'important': 'warning',
            'error': 'warning',
            'danger': 'warning',
        }

        admonition_type = confluence_admonition_map.get(name, 'info')

        macro = """\
            <ac:structured-macro ac:name="{admonition_type}">
              <ac:parameter ac:name="icon">true</ac:parameter>
              <ac:parameter ac:name="title"></ac:parameter>
              <ac:rich-text-body>
        """

        self.body.append(macro.format(admonition_type=admonition_type))

    def depart_admonition(self, node=None):
        macro = """
              </ac:rich-text-body>
            </ac:structured-macro>\n
        """
        self.body.append(macro)

    def imgtag(self, filename, suffix='\n', **attributes):
        """
        Attached image

        https://confluence.atlassian.com/display/DOC/Confluence+Storage+Format#ConfluenceStorageFormat-Images

        <ac:image>
        <ri:attachment ri:filename="atlassian_logo.gif" />
        </ac:image>

        Supported image attributes (some of these attributes mirror the equivalent HTML 4 IMG element):

        Name            Description
        ----            -----------
        ac:align        image alignment
        ac:border       Set to "true" to set a border
        ac:class        css class attribute.
        ac:title        image tool tip.
        ac:style        css style
        ac:thumbnail    Set to "true" to designate this image as a thumbnail.
        ac:alt          alt text
        ac:height       image height
        ac:width        image width

        """
        prefix = []
        atts = {}
        for (name, value) in attributes.items():
            atts[name.lower()] = value
        attlist = atts.items()
        attlist = sorted(attlist)
        parts = []
        src_part = '<ri:attachment ri:filename="%s" />' % filename
        for name, value in attlist:
            # value=None was used for boolean attributes without
            # value, but this isn't supported by XHTML.
            assert value is not None

            if isinstance(value, list):
                value = u' '.join(map(unicode, value))
            else:
                # First assume Python 2
                try:
                    value = unicode(value)
                # Otherwise, do it the Python 3 way
                except NameError:
                    value = str(value)

            parts.append('ac:%s="%s"' % (name.lower(), self.attval(value)))

        infix = '</ac:image>'
        return ''.join(prefix) + '<ac:image %s>%s%s' % (' '.join(parts), src_part, infix) + suffix

    def visit_image(self, node):
        atts = {}
        uri = node['uri']
        filename = os.path.basename(uri)
        atts['alt'] = node.get('alt', uri)
        atts['thumbnail'] = 'true'

        if 'width' in node:
            atts['width'] = node['width']

        if 'name' in node:
            atts['title'] = node['name']

        if (isinstance(node.parent, nodes.TextElement) or
            (isinstance(node.parent, nodes.reference) and
             not isinstance(node.parent.parent, nodes.TextElement))):
            # Inline context or surrounded by <a>...</a>.
            suffix = ''
        else:
            suffix = '\n'

        self.context.append('')
        self.body.append(self.imgtag(filename, suffix, **atts))

    def visit_title(self, node):
        if isinstance(node.parent, nodes.section) and not TitlesCache.has_title(self.document):
            h_level = self.section_level + self.initial_header_level - 1
            if h_level == 1:
                # Confluence take first title for page title from rst
                # It use for making internal links
                TitlesCache.set_title(self.document, node.children[0])

                # ignore first header; document must have title header
                raise nodes.SkipNode

        HTMLTranslator.visit_title(self, node)

    def visit_target(self, node):
        """
        Anchor Macro

        https://confluence.atlassian.com/display/DOC/Anchor+Macro

        <ac:structured-macro ac:name="anchor">
          <ac:parameter ac:name="">here</ac:parameter>
        </ac:structured-macro>
        """

        # Anchor confluence macros
        anchor_macros = """
            <ac:structured-macro ac:name="anchor">
              <ac:parameter ac:name="">%s</ac:parameter>
            </ac:structured-macro>
        """

        if 'refid' in node or 'refname' in node:

            if 'refuri' in node:
                link = node['refuri']
            elif 'refid' in node:
                link = node['refid']
            else:
                link = node['refname']

            self.body.append(anchor_macros % link)

    def depart_target(self, node):
        pass

    def visit_literal_block(self, node):
        """
        Code Block Macro

        https://confluence.atlassian.com/display/DOC/Code+Block+Macro

        <ac:structured-macro ac:name="code">
          <ac:parameter ac:name="title">This is my title</ac:parameter>
          <ac:parameter ac:name="theme">FadeToGrey</ac:parameter>
          <ac:parameter ac:name="linenumbers">true</ac:parameter>
          <ac:parameter ac:name="language">xml</ac:parameter>
          <ac:parameter ac:name="firstline">0001</ac:parameter>
          <ac:parameter ac:name="collapse">true</ac:parameter>
          <ac:plain-text-body><![CDATA[<b>This is my code</b>]]></ac:plain-text-body>
        </ac:structured-macro>
        """

        parts = ['<ac:structured-macro ac:name="code">']
        if 'language' in node:

            # Collapsible argument
            if node['language'] == 'collapse':
                parts.append('<ac:parameter ac:name="collapse">true</ac:parameter>')

            valid = ['actionscript3', 'bash', 'csharp', 'coldfusion', 'cpp', 'css', 'delphi', 'diff', 'erlang',
                     'groovy', 'html/xml', 'java', 'javafx', 'javascript', 'none', 'perl', 'php', 'powershell',
                     'python', 'ruby', 'scala', 'sql', 'vb']

            if node['language'] not in valid:
                node['language'] = 'none'

            parts.append('<ac:parameter ac:name="language">%s</ac:parameter>' % node['language'])

        if 'linenos' in node and node['linenos']:
            parts.append('<ac:parameter ac:name="linenumbers">true</ac:parameter>')

        parts.append('<ac:plain-text-body><![CDATA[%s]]></ac:plain-text-body>' % node.rawsource)
        parts.append('</ac:structured-macro>')

        self.body.append(''.join(parts))
        raise nodes.SkipNode

    def visit_download_reference(self, node):
        """
        Link to an attachment

        https://confluence.atlassian.com/display/DOC/Confluence+Storage+Format#ConfluenceStorageFormat-Links

        <ac:link>
          <ri:attachment ri:filename="atlassian_logo.gif" />
          <ac:plain-text-link-body><![CDATA[Link to a Confluence Attachment]]></ac:plain-text-link-body>
        </ac:link>
        """
        if 'filename' not in node:
            self.context.append('')
            return

        text = None
        if len(node.children) > 0 and len(node.children[0].children) > 0:
            text = node.children[0].children[0]

        parts = [
            '<ac:link>',
            '<ri:attachment ri:filename="%s" />' % node['filename'],
            '<ac:plain-text-link-body>',
            '<![CDATA[%s]]>' % text if text else '',
            '</ac:plain-text-link-body>',
            '</ac:link>',
        ]

        self.body.append(''.join(parts))
        raise nodes.SkipNode

    def visit_section(self, node):
        # removed section open tag
        self.section_level += 1

    def depart_section(self, node):
        # removed section close tag
        self.section_level -= 1

    def visit_reference(self, node):
        atts = {'class': 'reference'}
        if node.get('internal') or 'refuri' not in node:
            atts['class'] += ' internal'
        else:
            atts['class'] += ' external'
        if 'refuri' in node:
            atts['href'] = ''
            # Confluence makes internal links with prefix from page title
            if node.get('internal') and TitlesCache.has_title(self.document):
                atts['href'] += '#%s-' % TitlesCache.get_title(self.document).replace(' ', '')

            atts['href'] += node['refuri']
            if self.settings.cloak_email_addresses and atts['href'].startswith('mailto:'):
                atts['href'] = self.cloak_mailto(atts['href'])
                self.in_mailto = 1
        else:
            assert 'refid' in node, 'References must have "refuri" or "refid" attribute.'

            atts['href'] = ''
            # Confluence makes internal links with prefix from page title
            if node.get('internal') and TitlesCache.has_title(self.document):
                atts['href'] += '#%s-' % TitlesCache.get_title(self.document).replace(' ', '')
            atts['href'] += node['refid']

        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts['class'] += ' image-reference'
        if 'reftitle' in node:
            atts['title'] = node['reftitle']

        self.body.append(self.starttag(node, 'a', '', **atts))

        if node.get('secnumber'):
            self.body.append(('%s' + self.secnumber_suffix) % '.'.join(map(str, node['secnumber'])))

    def visit_desc(self, node):
        """ Replace <dl> """
        self.body.append(self.starttag(node, 'div', style="margin-top: 10px"))

    def depart_desc(self, node):
        self.body.append('</div>\n\n')

    def visit_desc_signature(self, node):
        """ Replace <dt> """
        # the id is set automatically
        self.body.append(self.starttag(
            node, 'div', style='margin-left: 20px; font-weight: bold;'))
        # anchor for per-desc interactive data
        if node.parent['objtype'] != 'describe' and node['ids'] and node['first']:
            self.body.append('<!--[%s]-->' % node['ids'][0])

    def depart_desc_signature(self, node):
        """ Copy-paste from original method """
        self.add_permalink_ref(node, _('Permalink to this definition'))
        self.body.append('</div>')

    def visit_desc_content(self, node):
        """ Replace <dd> """
        self.body.append(self.starttag(
            node, 'div', '', style='margin-left: 40px;'))

    def depart_desc_content(self, node):
        self.body.append('</div>')

    def visit_table(self, node):
        """ Fix ugly table border
        """
        self.context.append(self.compact_p)
        self.compact_p = True
        classes = ' '.join(['docutils', self.settings.table_style]).strip()
        self.body.append(
            self.starttag(node, 'table', CLASS=classes, border="0"))

    def write_colspecs(self):
        """ Fix ugly column width
        """
        pass


class ImageConf(images.Image):
    """
    Image confluence directive
    """

    def run(self):
        # remove 'align' processing
        # remove 'target' processing

        self.options.pop('align', None)
        reference = directives.uri(self.arguments[0])
        self.options['uri'] = reference
        set_classes(self.options)
        image_node = nodes.image(self.block_text, **self.options)
        self.add_name(image_node)
        return [image_node]


class TocTree(Directive):
    """
        Replace sphinx "toctree" directive to confluence macro

        Table of Contents Macro

        https://confluence.atlassian.com/display/DOC/Table+of+Contents+Macro

        <ac:structured-macro ac:name="toc">
          <ac:parameter ac:name="style">square</ac:parameter>
          <ac:parameter ac:name="minLevel">1</ac:parameter>
          <ac:parameter ac:name="maxLevel">3</ac:parameter>
          <ac:parameter ac:name="type">list</ac:parameter>
        </ac:structured-macro>
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'maxdepth': int,
        'name': directives.unchanged,
        'caption': directives.unchanged_required,
        'glob': directives.flag,
        'hidden': directives.flag,
        'includehidden': directives.flag,
        'titlesonly': directives.flag,
    }

    def run(self):
        macro = """
            <ac:structured-macro ac:name="toc">
              <ac:parameter ac:name="style">square</ac:parameter>
              <ac:parameter ac:name="minLevel">1</ac:parameter>
              <ac:parameter ac:name="maxLevel">3</ac:parameter>
              <ac:parameter ac:name="type">list</ac:parameter>
            </ac:structured-macro>\n
        """

        attributes = {'format': 'html'}
        raw_node = nodes.raw('', macro, **attributes)
        return [raw_node]


class JiraIssuesDirective(Directive):
    """
    JIRA Issues Macro

    https://confluence.atlassian.com/doc/jira-issues-macro-139380.html

    <ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="da6b6413-0b93-4052-af90-dbb252175860">
        <ac:parameter ac:name="server">Atlassian JIRA (JAC)</ac:parameter>
        <ac:parameter ac:name="columns">key,summary,created</ac:parameter>
        <ac:parameter ac:name="maximumIssues">20</ac:parameter>
        <ac:parameter ac:name="jqlQuery">project = CONF AND FixVersion=5.8 </ac:parameter>
        <ac:parameter ac:name="serverId">146780e9-1234-312f-1243-ed0555666fa</ac:parameter>
    </ac:structured-macro>
    """
    required_arguments = 1
    has_content = False
    final_argument_whitespace = True

    option_spec = {
        "anonymous": true_false,
        "server_id": directives.unchanged,
        "baseurl": directives.unchanged,
        "columns": directives.unchanged,
        "count": true_false,
        "height": directives.positive_int,
        "title": directives.unchanged,
        "render_mode": static_dynamic,
        "url": directives.unchanged,
        "width": directives.unchanged,
        "maximum_issues": directives.positive_int
    }

    def run(self):
        result = ['<ac:structured-macro ac:name="jira" ac:schema-version="1">']
        param_macro = '<ac:parameter ac:name="{name}">{value}</ac:parameter>'

        for name, value in self.options.items():
            result.append(param_macro.format(name=underscore_to_camelcase(name), value=value))

        jql_query = self.arguments[0]
        result.append(param_macro.format(name='jqlQuery', value=jql_query))

        result.append('</ac:structured-macro>')
        attributes = {'format': 'html'}

        raw_node = nodes.raw('', '\n'.join(result), **attributes)
        return [raw_node]


class JiraIssueRole(roles.GenericRole):

    def __call__(self, role, rawtext, text, *args, **kwargs):
        macro = """\
          <ac:structured-macro ac:name="jira" ac:schema-version="1">
            <ac:parameter ac:name="key">{key}</ac:parameter>
            <ac:parameter ac:name="showSummary">false</ac:parameter>
          </ac:structured-macro>
        """
        attributes = {'format': 'html'}
        return [nodes.raw('', macro.format(key=text), **attributes)], []


class JiraUserRole(roles.GenericRole):
    def __call__(self, role, rawtext, text, *args, **kwargs):
        macro = """\
        <ac:link>
            <ri:user ri:username="{username}"/>
        </ac:link>
        """
        attributes = {'format': 'html'}
        return [nodes.raw('', macro.format(username=text), **attributes)], []


def underscore_to_camelcase(text):
    return ''.join(word.title() if i else word for i, word in enumerate(text.split('_')))


def get_path():
    from os import path
    package_dir = path.abspath(path.dirname(__file__))
    template_path = path.join(package_dir, 'themes')
    return template_path


def setup(app):
    """
    :type app: sphinx.application.Sphinx
    """
    app.config.html_theme_path = [get_path()]
    app.config.html_theme = 'confluence'
    app.config.html_scaled_image_link = False
    app.config.html_translator_class = 'sphinx_confluence.HTMLConfluenceTranslator'
    app.config.html_add_permalinks = ''

    jira_issue = JiraIssueRole('jira_issue', nodes.Inline)
    app.add_role(jira_issue.name, jira_issue)

    jira_user = JiraUserRole('jira_user', nodes.Inline)
    app.add_role(jira_user.name, jira_user)

    app.add_directive('image', ImageConf)
    app.add_directive('toctree', TocTree)
    app.add_directive('jira_issues', JiraIssuesDirective)
    app.add_builder(JSONConfluenceBuilder)
