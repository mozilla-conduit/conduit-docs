#################################
Linux Arcanist Installation Guide
#################################

Arcanist and moz-phab can be installed into any location on your system, as
long as the ``arc`` and ``moz-phab`` commands work from your command line.

In this guide we'll be installing arc and moz-phab into ``~/.mozbuild``,
however they can be installed into any reasonable location.

Ensure PHP and git are installed
--------------------------------

Verify that both php and git are installed and working when run from the
command line:

.. code-block:: bash

    $ git --version
    git version 2.20.1
    $ php --version
    PHP 7.1.23 (cli) (built: Nov  7 2018 18:20:35) ( NTS )

The versions you have do not need match the above.

If either are missing use your distro's package manager to install.  For example
if you use Ubuntu:

.. code-block:: bash

    sudo apt-get install php php-curl git

Note Arcanist requires the ``ext-curl`` and other PHP extensions which may not be
enabled by default on your Linux distro.  For example Ubuntu requires that you
install the ``php-curl`` package, while Fedora also require the ``php-json`` package.


Install Arcanist
----------------

#. Create a ``~/.mozbuild`` directory if it doesn't already exist and clone the
   arcanist and phabricator library repositories:

.. code-block:: bash

    mkdir -p ~/.mozbuild
    cd ~/.mozbuild
    git clone https://github.com/phacility/arcanist.git
    git clone https://github.com/phacility/libphutil.git


Install moz-phab
----------------

#. Create a ``~/.mozbuild/moz-phab`` directory and download the latest version of
   ``moz-phab``:

.. code-block:: bash

    mkdir -p ~/.mozbuild/moz-phab
    cd ~/.mozbuild/moz-phab
    curl -O https://raw.githubusercontent.com/mozilla-conduit/review/$(basename $(curl -sLo /dev/null -w '%{url_effective}' https://github.com/mozilla-conduit/review/releases/latest))/moz-phab
    chmod +x moz-phab

Add arc and moz-phab to your PATH
---------------------------------

Both `arc` and `moz-phab` need to be on the PATH in order for the scripts to
work. Be aware the profile file varies between distros and shells
(eg. ``~/.bashrc`` instead of ``~/.profile``)

1. Update your ``PATH`` to include arcanist and moz-phab:

.. code-block:: bash

    echo 'export PATH="$HOME/.mozbuild/arcanist/bin:$HOME/.mozbuild/moz-phab:$PATH"' >> ~/.profile

2. Close and reopen your terminal program

3. Ensure running `arc` and `moz-phab` both work:

.. code-block:: bash

    arc -h
    moz-phab -h
