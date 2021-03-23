
.. _API:
.. index:: Python API

Python API
==========

The core of the IDP-Z3 software is a Python component `available on Pypi <https://pypi.org/project/idp-engine/>`_.
The following code illustrates how to invoke it.

.. code-block:: python

    from idp_engine import IDP, model_expand
    kb = IDP.parse("path/to/file.idp")
    T, S = kb.get_blocks("T, S")
    for model in model_expand(T,S):
        print(model)

Besides the methods and class available in the :ref:`main block<main>`, ``idp_engine`` exposes the ``IDP class``, described below.

IDP class
+++++++++

The ``IDP`` class exposes the following methods:

parse(file_or_string)
    This class method parses the :ref:`IDP program<IDP>` in the file or string.

get_blocks(names)
    This instance method returns the list of blocks whose names are given in a comma-separated string.


