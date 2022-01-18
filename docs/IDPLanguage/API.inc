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

The file ``path/to/file.idp`` must contain an :ref:`FO-dot <FO-dot>` knowledge base (with vocabulary, theory and, optionally, structure blocks).


``idp_engine`` exposes :ref:`useful functions <IDP_functions>`, as well as the ``Theory`` (described :ref:`here <Theory_class>`) and ``IDP`` classes.


IDP class
+++++++++

The ``IDP`` class exposes the following methods:

.. autoclass:: idp_engine.Parse.IDP
    :members:

.. _Theory:
