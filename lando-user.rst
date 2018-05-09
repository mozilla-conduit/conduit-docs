################
Lando User Guide
################

***********
About Lando
***********

Lando is Mozilla's new automatic code-landing service.  It is loosely
integrated with our `Phabricator instance
<https://phabricator.services.mozilla.com>`_.  Its purpose is to
easily commit Phabricator revisions to their destination repository.

*****
Usage
*****

All revisions in Phabricator have a "View in Lando" link.  If the
revision has been accepted (approved), the link will be active;
otherwise, it will be greyed out.  An active link looks like the
following:

.. image:: images/view-in-lando.png
   :align: center
   :alt: Screenshot of a Phabricator Revision ready to land with Lando

Clicking this link will take you to the Lando page for that revision:

.. image:: images/lando-land-it.png
   :align: center
   :alt: Screenshot of a revision in Lando that is ready to land

You can also go directly to a revision's Lando page by specifying the
revision ID in the Lando URL:
``https://lando.services.mozilla.com/revisions/D<rev number>/``.

A relevant set of metadata about the revision is presented, including
the diff ID (with a link back to Phabricator), the author, the status
of reviews, and the commit message.  There is also a timeline of
previous landing attempts, if any.

You must be logged in to initiate a landing.  Logins are handled by
Auth0 and follow the same flow as many other Mozilla systems.  In
addition to logging in, the following conditions must be true:

* The revision must be associated with a repository in Phabricator.
* A destination repository must be configured in Lando.
* You must have the required SCM permissions to land to the
  destination repo (e.g. ``scm_level_3`` for ``mozilla-central``).
* Your permissions for the repo must be active (i.e. not expired).
* A landing for this revision must not already be in progress.

If any of the above are not true, you will be shown an appropriate
error message at the bottom of the page, and the "Land" button will
not be displayed:

.. image:: images/lando-revision-not-associated-error.png
   :align: center
   :alt: Screenshot of a Lando error

If all the necessary conditions are met, a green "Land" button will be
displayed.  Take care to verify the information presented to ensure
that the commit will represent the correct information and that the
correct reviews have been granted.

There may also be one or more warnings, for example, if you previously
landed this revision.  You can acknowledge these errors if you believe
the landing should proceed regardless; to continue the example, if the
original commit had been backed out, you may indeed want to try
landing it again.

Once "Land" is clicked, a request will be queued.  Generally, this
will execute quickly, but if there are a lot of pending landings, or
if the trees are closed, it may take longer.  The landing request will
stay in the queue until it is executed.

Once the landing is executed, the timeline will be updated with the
results.

.. image:: images/lando-successful-landing.png
   :align: center
   :alt: Screenshot of the Lando timeline of a successful landing

.. note:: Lando pages do not currently automatically refresh; you will
          have to reload them manually to see updates.  There is a
          `bug
          <https://bugzilla.mozilla.org/show_bug.cgi?id=1460364>`_
          open to fix this.

If the landing failed, an error message will be displayed.  This error
may represent a problem with the revision, e.g. a merge conflict.  In
this case, the revision will have to be updated and resubmitted.  If
it appears to be an error with Lando itself (or related services),
please let us know in #lando on IRC or `file a bug
<https://bugzilla.mozilla.org/enter_bug.cgi?product=Conduit&component=Lando>`_.

