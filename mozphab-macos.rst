################################
macOS MozPhab Installation Guide
################################

MozPhab can be installed from PyPI

This requires Git, Python 3.5 or higher with `pip`, and PHP.

Install Python3 using Homebrew
------------------------------
1. Follow the instructions on https://brew.sh/ if Homebrew is not installed.

2. Install Python 3 and Pip with one command::

   $ brew install python


Install MozPhab
---------------
1. Call ``pip3 install MozPhab``

   Please note the first ``moz-phab`` call will install the Arcanist and its requirements
   under the ``~/.mozbuild/mozphab`` directory.

2. Ensure running ``arc`` and ``moz-phab`` both work:

.. code-block:: bash

    $ moz-phab arc -h
    $ moz-phab -h
