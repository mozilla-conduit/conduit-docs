################################
Linux MozPhab Installation Guide
################################

MozPhab can be installed from PyPI.

This requires Git and Python 3.5 or higher with ``pip3``.

Ensure the requirements are installed
-------------------------------------

Verify that pip3 and git are installed and working when run from the
command line:

.. code-block:: bash

    $ git --version
    git version 2.20.1
    $ pip3 --version
    pip 18.1 from /usr/lib/python3/dist-packages/pip (python 3.7)

The versions you have do not need match the above.

If either are missing use your distro's package manager to install.  For example
if you use Ubuntu:

.. code-block:: bash

    $ sudo apt-get install git python3-pip


Install MozPhab
---------------
1. Call ``pip3 install --user MozPhab``

   This will install ``moz-phab`` into your home directory, under ``~/.local/bin``.

2. If ``moz-phab`` has not been found, add your ``~/.local/bin`` directory to
   the ``PATH`` variable. Running this command in terminal will change the ``PATH``
   for current session. Add it to your profile file (``~/.bashrc`` or equivalent)
   to keep the ``$PATH`` changed ::

.. code-block:: bash

   $ export PATH=~/.local/bin:$PATH

3. Ensure running ``moz-phab`` works::

.. code-block:: bash

   $ moz-phab -h
