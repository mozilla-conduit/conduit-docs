###################################
Windows Arcanist Installation Guide
###################################

The `official Windows installation guide
<https://secure.phabricator.com/book/phabricator/article/arcanist_windows/>`_
for Arcanist is a bit confusing and vague.  Here are step-by-step
instructions to getting Arcanist working on Windows 10 in a
`MozillaBuild <https://wiki.mozilla.org/MozillaBuild>`_ environment.
They should work for Git Bash and PowerShell as well.

#. Install the Microsoft Visual C++ 2017 Redistributable (x64) if you
   don't already have it. You can see if you have it through Settings
   -> Apps -> App & features. It is available at
   https://support.microsoft.com/en-ca/help/2977003/the-latest-supported-visual-c-downloads
   (vc_redist.x64.exe).
#. Install PHP. The latest should work, e.g. PHP 7.2, VC15 x64 Non
   Thread Safe, from https://windows.php.net/download/. Download the
   Zip. Unzip it somewhere; the following instructions presume C:\\PHP.
#. Copy php.ini-development to php.ini in that same directory.
#. Edit php.ini. The Arcanist docs say to remove the leading ``;``
   before ``;extension=php_curl.dll``. In PHP 7.2, this line is
   just ``;extension=curl``. Then find the line ``;extension_dir =
   "ext"`` and change it to ``extension_dir = "C:\PHP\ext"``.
#. Run ``C:\PHP\php.exe -i`` to verify that it is working. You should see
   "curl" listed in the Configuration section.
#. If you don't have Git already installed (note that it is not
   currently packaged with MozillaBuild), you'll need to grab it from
   https://git-scm.com/download/win and install it.
#. Clone the libphutil and arcanist Git repositories somewhere. These
   docs presume a subdirectory, ``phabricator``, in your home directory,
   e.g. ``C:\Users\myuser\phabricator``.

   .. code-block:: bash

     mkdir phabricator
     cd phabricator
     git clone https://github.com/phacility/libphutil.git
     git clone https://github.com/phacility/arcanist.git

   Replace the last URL with
   ``https://github.com/mozilla-conduit/arcanist`` if you are using
   git-cinnabar.

#. Add ``arc`` and ``php`` to your user's path. If you use MSYS
   (including MozillaBuild) exclusively, you can add this to
   ``~/.bash_profile``::

     export PATH="$PATH:/c/php:~/phabricator/arcanist/bin"

   You can also add it to your user's path so that it is also
   recognized in PowerShell and other apps.  The easiest way to find
   this setting is to type "environment variables" into the search bar
   at the bottom of the desktop, and select "Edit environment
   variables for your account".  You can also get to it via the
   Control Panel > All Control Panel Items > System > Advanced System
   Settings > Environment Variables...

     #. Select the "Path" variable under "User variables for <user>".
     #. Click "Edit..."
     #. Click "New"
     #. Add ``C:\PHP``
     #. Click "New"
     #. Add ``%USERPROFILE%\phabricator\arcanist\bin``

#. Verify this all works with ``arc help``. You should see Arcanist's
   usage instructions.
#. Ensure you have an editor installed that has a "blocking mode" (not
   Notepad). MozillaBuild comes with vim, but there are other options,
   including Notepad++ and Sublime.
#. Tell Arcanist about your editor:

   #. If you only use MSYS/MozillaBuild, you can just add ``export
      EDITOR=/usr/bin/vim`` to your ``.bash_profile``.
   #. If you want to use vim but also want it available elsewhere
      (e.g. PowerShell), run

      .. code-block:: bash

        arc set-config editor "\"C:\Program Files\Git\usr\bin\vim.exe\""

   #. If you'd like to use another editor, replace the path in the
      above command with the path to that editor. For some editors,
      you may need other command line options, e.g.

      * Notepad++:

      .. code-block:: text

          arc set-config editor "\"C:\Program Files (x86)\Notepad++\notepad++.exe\" -multiInst -nosession"

      * Sublime Text 2:

      .. code-block:: text

          arc set-config editor "\"C:\Program Files\Sublime Text 2\sublime_text.exe\" -w -n"

      * Sublime Text 3:

      .. code-block:: text

          arc set-config editor "\"C:\Program Files\Sublime Text 3\subl.exe\" -w -n"

#. At this point, you should be all set up. Follow the rest of the
   standard instructions for :ref:`configuring Arcanist
   <setting-up-arcanist>` to use our instance.

