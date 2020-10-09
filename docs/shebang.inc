.. index:: Shebang

Shebang
-----------

The first line of an IDP program may be a `shebang <https://en.wikipedia.org/wiki/Shebang_(Unix)>`_ line, specifying the version of IDP-Z3 to be used.  
When a version is specified, the Interactive Consultant and Web IDE will be redirected to a server on the web running that version.  
The list of versions is available `here <https://gist.github.com/pcarbonn/662a3e8d148e0a1a4e1f04fdaccc0dcd>`_.
(The IDP-Z3 executable ignores the shebang.)

Example: :code:`#! IDP-Z3 0.5.4`