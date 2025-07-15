################################
macOS MozPhab Installation Guide
################################

MozPhab can be installed from PyPI

This requires Git and Python 3.6 or higher with `pip`.

.. note::

    There isn't a `moz-phab` wheel for all macOS systems, so you may need to install Rust so that `pip` can build `moz-phab` itself. Users of Mac computers with Apple silicon may need to ensure that Python version 3.9.1 or newer is installed to run `moz-phab` scripts with Python natively.

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
