.. _IDP:

.. role:: raw-html(raw)
   :format: html

IDP-Z3
======

IDP-Z3 is used to perform reasoning on FO[:raw-html:`&#183`] knowledge bases.
It can be invoked in 3 ways:

    - via a web interface, called webIDE.

    - in a shell, using the Command Line Interface of IDP-Z3.

    - in a Python program: by using classes and functions imported from the ``idp_engine`` package available on `Pypi <https://pypi.org/project/idp-engine/>`_.

These methods are further described below.

.. warning::
    An `FO-dot` program is a text file containing only
    `vocabulary, theory` and, `structure` blocks, as described in :ref:`FO-dot <FO-dot>`.
    An `IDP` program may additionally contain a `main()` procedure block, with instructions to process the FO-dot program.
    This procedure block is described later in this chapter.


.. include:: IDPLanguage/webIDE.inc
.. include:: IDPLanguage/CLI.inc
.. include:: IDPLanguage/API.inc