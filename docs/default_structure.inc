.. index:: default structure

.. _default_structure:

Default Structure
-----------------

The *default structure* functions similarly to a normal :ref:`structure`, in the sense that it can be used to set values of symbols.
However, these values are set as if they were given by the user: they are shown in the interface as selected values.
The symbols can still be assigned different values, or they can be unset.

In this way, this type of structure is used to form a *default* set of values for symbols.
Such a structure is given the name 'default', to denote that it specifies default values.
The syntax of the block remains the same.

.. code::

    structure default {
        // here comes the structure
    }
