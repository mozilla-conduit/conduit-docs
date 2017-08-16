############
Conduit Docs
############

This repository holds documentation for the various parts of Mozilla's
`Conduit project
<https://wiki.mozilla.org/EngineeringProductivity/Projects/Conduit>`_,
which provides tools, services, and automation relating to the
submission, review, and landing of patches to the Firefox codebase.

To build these docs, you will need Sphinx and a machine running Linux,
OS X, or the Windows 10 Linux Subsystem.  If you don't want to install
Sphinx at the system level, you can use a virtualenv.  For example::

  $ virtualenv venv
  Running virtualenv with interpreter /usr/bin/python2
  New python executable in /home/mcote/projects/conduit-docs/venv/bin/python2
  Also creating executable in /home/mcote/projects/conduit-docs/venv/bin/python
  Installing setuptools, pkg_resources, pip, wheel...done.
  
  $ . venv/bin/activate
  
  (venv) $ pip install Sphinx
  Collecting Sphinx
    Using cached Sphinx-1.6.3-py2.py3-none-any.whl
  Collecting sphinxcontrib-websupport (from Sphinx)
    Using cached sphinxcontrib_websupport-1.0.1-py2.py3-none-any.whl
  ... lots more text ...
  Successfully installed Jinja2-2.9.6 MarkupSafe-1.0 Pygments-2.2.0 Sphinx-1.6.3 alabaster-0.7.10 babel-2.4.0 certifi-2017.7.27.1 chardet-3.0.4 docutils-0.14 idna-2.6 imagesize-0.7.1 pytz-2017.2 requests-2.18.4 six-1.10.0 snowballstemmer-1.2.1 sphinxcontrib-websupport-1.0.1 typing-3.6.2 urllib3-1.22

You can then run ``make html`` to generate an HTML version of the
docs, which will be written to ``_build/html``.

These docs are hosted at https://moz-conduit.readthedocs.io/en/latest/
and are automatically built from the `source repo
<https://github.com/mozilla-conduit/conduit-docs>`_.
