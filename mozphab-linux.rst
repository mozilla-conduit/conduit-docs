################################
Linux MozPhab Installation Guide
################################

MozPhab can be installed from PyPI.

This requires Git, Python 3.5 or higher with ``pip3`` and PHP.

Ensure PHP and git are installed
--------------------------------

Verify that pip3, php and git are installed and working when run from the
command line:

.. code-block:: bash

    $ git --version
    git version 2.20.1
    $ php --version
    PHP 7.1.23 (cli) (built: Nov  7 2018 18:20:35) ( NTS )
    $ pip3 --version
    pip 18.1 from /usr/lib/python3/dist-packages/pip (python 3.7)

The versions you have do not need match the above.

If either are missing use your distro's package manager to install.  For example
if you use Ubuntu:

.. code-block:: bash

    $ sudo apt-get install php php-curl git python3-pip

Note Arcanist requires the ``ext-curl`` and other PHP extensions which may not be
enabled by default on your Linux distro.  For example Ubuntu requires that you
install the ``php-curl`` package, while Fedora also require the ``php-json`` package.


Install MozPhab
---------------
1. Call ``pip3 install --user MozPhab``

   This will install ``moz-phab`` into your home directory, under ``~/.local/bin``.

   Please note the first ``moz-phab`` call will install the Arcanist and its requirements
   under the ``~/.mozbuild/mozphab`` directory.

2. If ``moz-phab`` has not been found, add your ``~/.local/bin`` directory to
   the ``PATH`` variable. Running this command in terminal will change the ``PATH``
   for current session. Add it to your profile file (``~/.bashrc`` or equivalent)
   to keep the ``$PATH`` changed ::

.. code-block:: bash

   $ export PATH=~/.local/bin:$PATH

3. Ensure running ``arc`` and ``moz-phab`` both work::

.. code-block:: bash

   $ moz-phab arc -h
   $ moz-phab -h
