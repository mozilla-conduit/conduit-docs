################################
macOS MozPhab Installation Guide
################################

MozPhab can be installed from PyPI

This requires Git and Python 3.5 or higher with `pip`.

Install Python3 using Homebrew
------------------------------
1. Follow the instructions on https://brew.sh/ if Homebrew is not installed.

2. Install Python 3 and Pip with one command::

   $ brew install python


Install MozPhab
---------------
1. Call ``pip3 install MozPhab``

2. Ensure running ``moz-phab`` works:

.. code-block:: bash

    $ moz-phab -h
