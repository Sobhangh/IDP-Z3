.. _code_reference:

Appendix: IDP-Z3 internal reference
===================================


.. warning::
   This reference is only intended for the **core IDP-Z3 development team**.
   If you do not work on the IDP-Z3 engine itself, but just want to use it in your applications, please use our :ref:`API` instead.

The components of IDP-Z3 are shown below.

.. mermaid::

   graph TD
      webIDE_client --> IDP-Z3_server
      Interactive_consultant_client --> IDP-Z3_server
      Read_the_docs
      Homepage
      IDP-Z3_server --> IDP-Z3_engine
      IDP-Z3_command_line --> IDP-Z3_engine
      IDP-Z3_engine --> Z3

* `webIDE <https://interactive-consultant.idp-z3.be/IDE>`_  client: browser-based application to edit and run IDP-Z3 programs
* `Interactive Consultant <https://interactive-consultant.idp-z3.be/>`_  client: browser-based user-friendly decision support application
* `Read_the_docs <http://docs.idp-z3.be/en/stable/>`_ : online documentation
* `Homepage <https://www.idp-z3.be/>`_
* IDP-Z3 server: web server for both web applications
* IDP-Z3 command line interface
* IDP-Z3 engine: performs reasoning on IDP-Z3 theories
* `Z3 <https://github.com/Z3Prover/z3>`_: `SMT solver <https://en.wikipedia.org/wiki/Satisfiability_modulo_theories>`_ developed by Microsoft

The `source code of IDP-Z3 <https://gitlab.com/krr/IDP-Z3>`_ is publicly available under the GNU LGPL v3 license.
You may want to check the `Development and deployment guide <https://gitlab.com/krr/IDP-Z3/-/wikis/Development-and-deployment-guide>`_.


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   Architecture.md
   Diagrams.md
   idp_engine.rst
   idp_web_server.rst

