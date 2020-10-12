.. index:: Shebang

Shebang
-----------

The first line of an IDP program may be a `shebang <https://en.wikipedia.org/wiki/Shebang_(Unix)>`_ line, specifying the version of IDP-Z3 to be used.  
When a version is specified, the Interactive Consultant and Web IDE will be redirected to a server on the web running that version.  
The list of versions is available `here <https://gist.github.com/IDP-Z3/5d82c61fa39e8aa23da1642a2e2b420a>`_.
(The IDP-Z3 executable ignores the shebang.)

Example: :code:`#! IDP-Z3 0.5.4`