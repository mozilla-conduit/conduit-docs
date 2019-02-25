*********************************
Phabricator Workflow Walk-through
*********************************

**IMPORTANT:** Make sure you have :ref:`set up Phabricator <creating-account>` and
:ref:`set up Arcanist <setting-up-arcanist>` before proceeding!

While some developers use bookmarks/etc to track changes, for this this guide we will
use just repository heads: no bookmarks or labels.  This essentially means "just
start coding off tip and commit". The ``hg wip`` alias provides a view of the
repository that allows for keeping track of the work.

(If you want to dig deeper into the "to label or not to label" discussion,
see `this document <https://mozilla-version-control-tools.readthedocs.io/en/latest/hgmozilla/workflows.html#to-label-or-not-to-label>`_)

Landing a commit to mozilla-central
===================================

For this example we will craft one change for review.  When we get feedback that changes
are required we will amend our commit in-place.

We'll use:

* One commit
* One review request per commit
* ``hg amend`` to add fix-ups to our commit
* ``moz-phab`` to request code reviews


Fixing the code
---------------

Let's start with a clean checkout.

::

    $ hg wip
    @    460880 tip Merge inbound to mozilla-central.  a=merge
    |\
    ~ ~

    $ vim dom/audiochannel/AudioChannelAgent.cpp
    # hack hack

    $ hg status
    M dom/audiochannel/AudioChannelAgent.cpp

When we write the commit message we should follow the Firefox source tree's common
commit message format.  We will include a Bug ID and list of reviewers.  See the
`committing rules <https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Committing_Rules_and_Responsibilities#Commit_message_restrictions>`_
for more information about proper commit message formatting.

::

  $ hg commit
  Bug 1445923 - WebAudio: Remove b2g dead code r?sylvestre


  Removed dead code from ...

* You are allowed to skip the bug number and reviewer names if you don't have them yet,
  but the `Lando automated landing system <https://lando.services.mozilla.com/>`_,
  used later in this walk-through, will insist that you add them before the code can
  be landed.


Requesting a Review
-------------------

Before we request a review we should check for changes upstream.

::

    $ hg pull --rebase

The ``moz-phab`` command will take care of creating a code review for us.  It will
automatically link the review to the BMO bug as well as notifying the reviewers.

::

    $ moz-phab
    Submitting 1 commit:
    (New) 460880:e376ef5bf453 Bug 1445923 - WebAudio: Remove b2g dead code r?sylvestre
    Submit to Phabricator (YES/No/Always)?

    ...

    Completed
    (D55555) 460880:e376ef5bf453 Bug 1445923 - WebAudio: Remove b2g dead code r?sylvestre
    -> https://phabricator.services.mozilla.com/D55555


Addressing feedback
-------------------

When it's time to address feedback we use ``hg amend``.

* ``hg commit --amend`` also works, and allows you to update the commit description
  while amending the commit.

::

    $ hg wip
    @  460881 tip Bug 1445923 - WebAudio: Remove b2g dead code r?sylvestre
    o    460880 Merge inbound to mozilla-central.  a=merge
    |\
    ~ ~


    $ hg checkout 460881
    $ vim dom/audiochannel/AudioChannelAgent.cpp
    # fixup fixup

    $ hg amend


Check off the Done item in the Phabricator UI.

.. image:: images/review-item-done.png
   :width: 800
   :align: center
   :alt: Screenshot of a Done review item


Now run ``moz-phab`` a second time.  Phabricator will automatically submit your Done
items in the UI and notify your reviewers that you have made updates.


::

    $ moz-phab


Landing the changes
-------------------

Everything looks good: the reviewers have approved our changes. Let's land our
changes.

On your revision page in Phabricator click the "View Stack in Lando" link in the
right-hand menu:

.. image:: images/view-in-lando.png
   :width: 800
   :align: center
   :alt: Screenshot of a Phabricator Revision ready to land with Lando


You will be taken to the Lando revision overview page.  Press "Preview Landing" and give
the change one last review: double-check the commit message, etc., before hitting the
"Land" button.

.. image:: images/lando-land-it.png
   :width: 800
   :align: center
   :alt: Screenshot of a revision in Lando that is ready to land

Hit the "Land" button and Lando will automatically land your changes.

Where to go from here
=====================

``moz-phab`` has other features including the ability to update and land entire stacks
of related commits.  Check out the :ref:`Submitting Patches <using-moz-phab>` section
for more information.
