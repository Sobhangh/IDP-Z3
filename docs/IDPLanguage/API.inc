.. _api:

Python API
----------

The core of the IDP-Z3 software is a Python component `available on Pypi <https://pypi.org/project/idp-engine/>`_.
The following code illustrates how to invoke it.

.. code-block:: python

    from idp_engine import IDP, Theory, duration
    kb = IDP.from_file("path/to/file.idp")
    T, S = kb.get_blocks("T, S")
    theory = Theory(T, S)
    for model in theory.expand():
        print(model)
    duration("End")


``idp_engine`` exposes the ``IDP`` and ``Theory`` classes, as well as some useful functions.
They are described below.

IDP class
+++++++++

The ``IDP`` class exposes the following methods:

.. autoclass:: idp_engine.Parse.IDP
    :members:

.. _Theory:


Theory class
+++++++++++++

Instances of the ``Theory`` class represent a collection of theory and structure blocks.

Many operations on Theory instances can be chained, e.g., ``Theory(T,S).propagate().simplify().formula()``.

The class has the following methods:

.. autoclass:: idp_engine.Problem.Theory
    :members:

.. _idp_engine:

``idp_engine`` functions
++++++++++++++++++++++++


.. automodule:: idp_engine.Run
    :members:
