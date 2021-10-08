Introduction
============

IDP-Z3 is a reasoning engine for knowledge represented using the FO(.) language.

FO(.) is First Order logic, with various extensions to make it more expressive: types, arithmetic, inductive definitions, aggregates, and intensional objects.

Once the knowledge of a problem domain is encoded in FO(.), the engine can perform a variety of reasoning tasks: find relevant questions to solve a particular problem, derive consequences from new information, explain how it derived these consequences, find a solution that minimizes a cost function, ...

IDP-Z3 is developed by the Knowledge Representation group at KU Leuven in Leuven, Belgium, and made available under the `GNU LGPL v3 License <https://www.gnu.org/licenses/lgpl-3.0.txt>`_.
It uses the `Microsoft Z3 solver <https://github.com/Z3Prover/z3>`_ as back-end to perform the reasoning tasks.
(The previous version of the reasoning engine, `IDP3 <https://dtai.cs.kuleuven.be/drupal/software/idp>`_, used minisat)

Projects
--------
The IDP-Z3 reasoning engine is currently deployed in the following open-source projects:

* the `Interactive Consultant <interactive_consultant.html>`_, a tool enabling experts to encode their knowledge of a problem domain, and to automatically create an interactive web tool that helps end users find solutions for specific problems in that domain.
* `DMN-IDP <https://dmn-idp.herokuapp.com/>`_, a user-friendly tool which combines the readability of the Decision Model and Notation (DMN) standard with the power of the IDP system through an interactive interface.

IDP-Z3 has also been used in private projects by Saint-Gobain, Flanders Make, and a partner in the financial sector, among others.
These projects use a data-poor, knowledge-rich approach to Artificial Intelligence to leverage the knowledge of the experts in their fields.

Our partners particularly appreciate the ease of encoding this knowledge in FO(.): its expressivity removes a long-standing barrier in the use of Knowledge Base systems.

Get in touch?
-------------
The IDP-Z3 engine is available for experimentation through its `online IDE <https://interactive-consultant.IDP-Z3.be/IDE>`_.
Its documentation is available `online <https://docs.idp-z3.be/en/stable/>`_, including a guide on how to install the IDP-Z3 system for use offline.
For further support or other inquiries, you can contact us `by mail <mailto:krr@kuleuven.be>`_.
