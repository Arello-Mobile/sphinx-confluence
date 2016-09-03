==============
Document Title
==============

.. toctree::
     :maxdepth: 2

     example


Chapter 1 Title
===============

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer egestas commodo lorem. Vivamus urna odio, vehicula
et blandit ut, accumsan vitae ipsum. Fusce lobortis, ligula vitae hendrerit elementum, urna leo ultrices risus, eget
rhoncus nibh leo sit amet orci. Fusce fermentum consectetur neque, vitae varius leo euismod commodo. Curabitur vitae
efficitur lacus. Nunc ut ex non nibh lacinia pulvinar. Sed vel tempor felis, in tincidunt neque. Pellentesque tellus
tortor, pulvinar vel accumsan vitae, condimentum hendrerit eros. Integer pretium placerat laoreet. Aliquam erat
volutpat.

Section 1.1 Title
-----------------

* Lorem ipsum dolor sit amet
* Nulla dictum pretium turpis,
  quis volutpat odio ornare eget

1. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
2. Ut sit amet vehicula nunc.

#. Mauris luctus sapien in odio consequat dapibus.
#. Curabitur sit amet venenatis justo.

Subsection 1.1.1 Title
~~~~~~~~~~~~~~~~~~~~~~

* Etiam interdum
* mauris a ipsum

  * scelerisque pulvinar
  * et a nunc

* Proin in arcu elit

Section 1.2 Title
-----------------

Nulla nulla arcu, mattis et volutpat nec, bibendum in felis::

   Curabitur cursus maximus urna ut tristique. Pellentesque habitant morbi tristique senectus et netus et malesuada
   fames ac turpis egestas. Sed blandit consectetur risus vitae mattis. Donec at dapibus ipsum. Lorem ipsum
   dolor sit amet, consectetur adipiscing elit. Mauris aliquam libero et vehicula porttitor.

   Suspendisse nec odio nec risus dictum convallis at vel augue. Mauris aliquet eleifend leo eu lobortis.

Cras in imperdiet ipsum.


Chapter 2 Title
===============

Section 2.1 Title
-----------------

.. note:: Info macro example
   This text is rendered inside info macro rst "note"-directive is rendered as "info"

.. warning:: Note macro example
   This text is rendered inside note macro rst "warning"-directive is rendered as "note"

.. tip:: Tip macro example
   This text is rendered inside tip macro rst "tip"-directive is rendered as "tip"

.. danger:: Warning macro example
   - This text is rendered inside warning macro
   - rst "danger"-directive is rendered as "danger"

.. tip:: This text is rendered inside tip macro rst "tip"-directive is rendered as "tip"


Section 2.1 Title
-----------------

Lorem ipsum dolor sit amet, :jira_issue:`WDT-117` consectetur adipiscing elit. Ut sit amet vehicula nunc.
Nulla dictum pretium :jira_user:`Bob`, :jira_user:`Rob`, :jira_user:`John` turpis, quis volutpat odio ornare eget.

Section 2.2 Title
-----------------

.. jira_issues:: project = WDT AND issuetype = Epic AND resolution = Unresolved
   :title: Unresolved project epics
   :server_id: asd
   :columns: type;key;summary;status;created;
   :width: 80%
