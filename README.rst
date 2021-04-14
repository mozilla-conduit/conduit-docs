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

  $ python3 -m venv venv
  $ . venv/bin/activate
  (venv) $ pip3 install Sphinx
  Collecting Sphinx
  Downloading Sphinx-3.5.4-py3-none-any.whl (2.8 MB)
  ...

You can then run ``make html`` to generate an HTML version of the
docs, which will be written to ``_build/html``.

These docs are hosted at https://moz-conduit.readthedocs.io/en/latest/
and are automatically built from the `source repo
<https://github.com/mozilla-conduit/conduit-docs>`_.

File bugs in Bugzilla under `Conduit :: Documentation
<https://bugzilla.mozilla.org/enter_bug.cgi?product=Conduit&component=Documentation>`_
and submit patches via `Phabricator <https://phabricator.services.mozilla.com>`_.
