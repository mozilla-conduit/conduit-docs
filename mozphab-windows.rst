#####################################
Windows 10 MozPhab Installation Guide
#####################################

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
#. If you don't have Git already installed (note that it is not
   currently packaged with MozillaBuild), you'll need to grab it from
   https://git-scm.com/download/win and install it.
#. Run ``pip3 install MozPhab``.
#. Add ``moz-phab`` and ``git`` to the ``$PATH`` variable.
   If you use MSYS (including MozillaBuild) exclusively, you can add this to
   ``~/.bash_profile``::

     export PATH=$PATH:/c/Program\ Files/Git/bin:/c/mozilla-build/Python3/Scripts
     
#. Ensure running ``moz-phab`` works::

     $ moz-phab -h
