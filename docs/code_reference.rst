.. _code_reference:

Appendix: IDP-Z3 developer reference
====================================


.. note::
   The contents of this reference are intended for people who want to further develop IDP-Z3.

.. note::
   Despite our best efforts, this documentation may not be complete and up-to-date.

The components of IDP-Z3 are shown below.

.. mermaid::

   graph TD
      webIDE_client --> IDP-Z3_server
      Interactive_consultant_client --> IDP-Z3_server
      Read_the_docs
      Homepage
      IDP-Z3_server --> IDP-Z3_solver
      IDP-Z3_command_line --> IDP-Z3_solver
      IDP-Z3_solver --> Z3

* `webIDE <https://interactive-consultant.idp-z3.be/IDE>`_  client: browser-based application to edit and run IDP-Z3 programs
* `Interactive Consultant <https://interactive-consultant.idp-z3.be/>`_  client: browser-based user-friendly decision support application
* `Read_the_docs <http://docs.idp-z3.be/en/stable/>`_ : online documentation
* `Homepage <https://www.idp-z3.be/>`_
* IDP-Z3 server: web server for both web applications
* IDP-Z3 command line interface
* IDP-Z3 solver: performs inferences on IDP-Z3 theories
* `Z3 <https://github.com/Z3Prover/z3>`_: `SMT solver <https://en.wikipedia.org/wiki/Satisfiability_modulo_theories>`_ developed by Microsoft

The `source code of IDP-Z3 <https://gitlab.com/krr/IDP-Z3>`_ is publicly available under the GNU LGPL v3 license.


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   Architecture.md
   idp_solver.rst
   idp_server.rst

