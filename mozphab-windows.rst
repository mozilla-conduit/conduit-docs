#####################################
Windows 10 MozPhab Installation Guide
#####################################

----------------------
Installing MozPhab including ``arcanist`` setup
----------------------

Here are step-by-step instructions to getting MozPhab working on Windows 10 in a
`MozillaBuild <https://wiki.mozilla.org/MozillaBuild>`_ environment.
They should work for Git Bash and PowerShell as well. For the sake of this
documentation we will use the terminal provided by running
the ``C:\mozilla-build\start-shell.bat``.

#. Install the Microsoft Visual C++ 2017 Redistributable (x64) if you
   don't already have it. You can see if you have it through Settings
   -> Apps -> App & features. It is available at
   https://support.microsoft.com/en-ca/help/2977003/the-latest-supported-visual-c-downloads
   (vc_redist.x64.exe).
#. Add ``moz-phab``, ``php``, and ``git`` to the ``$PATH`` variable.
   If you use MSYS (including MozillaBuild) exclusively, you can add this to
   ``~/.bash_profile``::

     export PATH=$PATH:/c/PHP/:/c/Program\ Files/Git/bin:/c/mozilla-build/Python3/Scripts

#. Install PHP. The latest should work, e.g. PHP 7.2, VC15 x64 Non
   Thread Safe, from https://windows.php.net/download/. Download the
   Zip. Unzip it somewhere; the following instructions presume ``C:\PHP``.
#. Copy php.ini-development to php.ini in that same directory.
#. Edit php.ini. The Arcanist docs say to remove the leading ``;``
   before ``;extension=php_curl.dll``. In PHP 7.2, this line is
   just ``;extension=curl``. Then find the line ``;extension_dir =
   "ext"`` and change it to ``extension_dir = "C:\PHP\ext"``.
#. Run ``php -i`` to verify that it is working. You should see
   "curl" listed in the Configuration section.
#. If you don't have Git already installed (note that it is not
   currently packaged with MozillaBuild), you'll need to grab it from
   https://git-scm.com/download/win and install it. 
   
#. Run ``pip3 install MozPhab``. 

#. Ensure running ``arc`` and ``moz-phab`` both work::

     $ moz-phab arc -h
     $ moz-phab -h

   
----------------------
Upgrading a previous non-pip install of moz-phab to use pip
----------------------

#. Run ``pip3 install MozPhab``.

#. You may need to restart your shell for your changes to take effect. You can check using ``moz-phab version`` - if it works, you've successfully switched to ``moz-phab`` using ``pip``.

#. At this point, you should be all set up. If you have already installed ``moz-phab``
   without using ``pip``, you should remove the file.
