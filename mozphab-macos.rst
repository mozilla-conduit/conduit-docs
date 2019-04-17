################################
macOS MozPhab Installation Guide
################################

MozPhab can be installed with a simple `pip install MozPhab`.

This requires git, python with pip and php, which happily are preinstalled on macOS.

First `moz-phab` call will install the Arcanist and its requirements under the
`~/.mozbuild/mozphab` directory.

You can ensure running `arc` and `moz-phab` both work:

.. code-block:: bash

    moz-phab arc -h
    moz-phab -h
