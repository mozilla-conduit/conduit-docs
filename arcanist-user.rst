###################
Arcanist User Guide
###################

********
Arcanist
********

Mozilla's `Engineering Workflow
<https://wiki.mozilla.org/Engineering_Workflow>`_ team has created a
custom command-line tool, :ref:`moz-phab <using-moz-phab>`, which has
better support for submitting, updating, and applying series of
commits.  It also has conveniences for parsing bug IDs and reviewers
from commit-message summaries or specifying them as command-line
options.

This document is an older guide for Arcanist, the official upstream
command-line interface to Phabricator.  It may still be useful for
those who do not frequently submit patches for review.

This guide is a quick overview of how to submit, update, and apply
patches with Arcanist.  The official Phabricator documentation also
has an `Arcanist Quick Start guide
<https://phabricator.services.mozilla.com/book/phabricator/article/arcanist_quick_start/>`_,
a larger `Arcanist User Guide
<https://phabricator.services.mozilla.com/book/phabricator/article/arcanist/>`_,
and a specific `guide to "arc diff"
<https://phabricator.services.mozilla.com/book/phabricator/article/arcanist_diff/>`_.

There are a few ways to use Arcanist and Differential.  We'll cover
two common use cases: fix-up commits, which is somewhat similar to
GitHub's process, and amended commits, which is similar to MozReview's
model.

*******************************
Submitting and Updating Patches
*******************************

.. _initial-patch:

The Initial Patch
-----------------

Submitting the initial patch is the same in both processes.  First,
commit a change.  Here's an example::

    $ echo "Test" > PHABTEST
    $ hg add PHABTEST && hg commit -m "Add test file."

Then create a revision in Differential::

    $ arc diff

You'll be taken to an editor to add extra details.  Here is an example
of input to ``arc diff`` from a real revisino
(https://phabricator.services.mozilla.com/D1298):

.. code-block:: text

    heartbeat: check all backing services in heartbeat (Bug 1442911).

    Summary:

    Before this change /__heartbeat__ was only checking for connectivity
    to Phabricator. We now also check the database, transplant, redis
    (cache), s3, and auth0. The /__heartbeat__ endpoint now returns a more
    useful response, indicating which services are unhealthy when a 500
    response is sent.

    Test Plan:

    invoke test passes, new tests added. Ran lando api locally with
    services in both healthy and unhealthy states and observed the response
    from /__heartbeat__

    Reviewers: glob, imadueme

    Subscribers:

    Bug #: 1442911

Your commit message will be used to create the revision title and
summary.  The other fields are optional.  If they are given in a
similar format in the commit message, the fields will be prepopulated
here as well.  This includes ``Bug``; omitting a bug ID will result in
the revision not being associated with a bug, and thus it will
automatically be public.  If set, the field must contain a valid BMO
bug number.  Note that mozilla-central commit policy currently
`requires a bug number
<https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Committing_Rules_and_Responsibilities#Checkin_comment>`_
in the commit message under most circumstances.

Unfortunately, a limitation of Phabricator currently prevents us from
seeding this field with a bug ID from the commit message (at least
from the first line, where bug IDs are usually mentioned in
mozilla-central changesets).  Note that we have worked around these
restrictions in :ref:`moz-phab <using-moz-phab>`.

You may want to add a reviewer, which should be a Phabricator username
(e.g. ``mcote``).  You can also add one or more subscribers, who will
be notified of updates to the revision.  Again, we cannot parse these
out of the commit summary with Arcanist, but :ref:`moz-phab
<using-moz-phab>` supports this.

Note that the commits to be included in this revision are present in
the comment at the bottom of the text.  You can use this to double-check
that you are sending the correct commits to Phabricator.

After you exit the editor, the revision should be created.  Here's
example output from a different revision on our development instance:

.. code-block:: text

    Created a new Differential revision:
            Revision URI: https://mozphab.dev.mozaws.net/D29

    Included changes:
      A       PHABTEST

If you visit the revision at the provided URL, you will see that it is
labelled "Needs Review", which is the default state of a newly created
revision.  It will also be marked "Public", unless the bug ID you
entered is a confidential bug to which you have access.  For
convenience, an attachment is created on the bug containing just the
URL to the new revision, with the description being the revision's
title.  Finally, you will also see a few actions on the revision,
which are automatically performed by our BMO-integration code.  For
more on Phabricator-BMO integration, see :ref:`bmo-integration` in the
:doc:`Phabricator User Guide </phabricator-user>`.

.. _fix-up-commits:

Fix-Up Commits
--------------

After your patch has been reviewed, you may have to update your patch
and get another round of reviews.  As mentioned, there are two ways to
do this in Differential.

The "fix-up commit" model involves creating a new commit containing
the updates.  This is similar to GitHub's standard process.  You will
end up with a series of commits that should be "squashed" into a
single commit before landing, since the fix-up commits are not useful
history once a change has landed.

Here's an example that adds another line to our test file from above::

    $ echo "Update" >> PHABTEST
    $ hg commit -m "Update patch."

Submitting the change to Differential is the same command::

    $ arc diff

Your editor will again be opened, but this time the format is much
simpler.  You just need to provide a change summary, which again is
automatically seeded from your commit message.  Arcanist should also
have determined which revision to update.  If for some reason it was
not able to, you can use the ``--update`` option to specify a
revision ID.

After the update has been submitted, you will see output similar to
this:

.. code-block:: text

    Updated an existing Differential revision:
            Revision URI: https://mozphab.dev.mozaws.net/D29

    Included changes:
      A       PHABTEST

Going to the revision's URL will show the change in the activity log.
There will also be new entries in the "History" and "Commits" tabs in
the "Revision Contents" table.  You can use the History tab to switch
between various diff views: the current patch, the patch at a
particular point in history, and the changes between different
commits, i.e., an interdiff.  Here are the changes between the first
and second commit ("Diff 1" and "Diff 2" in Phabricator language):

.. image:: images/interdiff.png
   :align: center
   :alt: Screenshot of changes between Diff 1 and Diff 2

Amended Commits
---------------

The other method for updating patches is to amend the commits in
place.  This is similar to MozReview's standard process.

Starting from the end of the above section, :ref:`initial-patch`,
rather than creating a new commit, we amend the existing commit, like
so::

    $ echo "Update" >> PHABTEST
    $ hg commit --amend

After running ``arc diff``, an editor is again opened for a change
summary, although this time there is no new commit message to use, so
we must enter one manually.  Once the update is processed, the
revision looks very similar to the revision with fix-up commits,
except the "Commits" tab of the "Revision Contents" table has only a
single entry.  The "History" tab, however, is identical to the fix-up
commits scenario, with "Diff 1" and "Diff 2" entries, and the same
ability to see the different patches and differences between them.

.. _series-of-commits:

Series of Commits
-----------------

It is possible to chain a series of revisions together in
Differential, although it is currently a manual process.  This feature
can be used to represent a stack of commits to split up a complicated
patch, which is a good practice to make testing and reviewing easier.

To use this pattern, you will need to specify the exact commit you
want to send to Differential, since the default is to send all your
draft commits to a single revision, i.e., the :ref:`fix-up-commits`
method, which is not what we want here.  To send only the currently
checked-out Mercurial commit, run the following::

    $ arc diff .^

To set the parent-child relationship, you can use the UI or put a
directive into the child's commit message.  To use the UI, go to your
first commit, choose "Edit Related Revisions..." from the right-hand
menu, then "Edit Child Revisions".  Your child revision may be
suggested, or you can enter an ID into the search box, including the
``D`` to denote a differential revision, e.g. ``D32``:

.. image:: images/add-child-revision.png
   :align: center
   :alt: Screenshot of the dialog for adding a child revision

Select the appropriate revision and click "Save Child Revisions".  The
"Revision Contents" table will now have a new tab, "Stack", which
shows the current stack of revisions:

.. image:: images/revision-stack.png
   :align: center
   :alt: Screenshot of a revision stack

You can also add ``Depends on D<revision ID>`` to the child's commit
message, replacing ``<revision ID>`` with the ID of the parent
revision. (This needs to be its own paragraph, separated by a blank line.)
The relationship will be created when ``arc diff`` is run.

Unfortunately there is not currently a way to see a combined diff of
all the stacked commits together without applying the commits
locally.  Also, when you update any commits, you'll need to run ``arc
diff .^`` for each child commit as well.  This was the primary purpose of
writing :ref:`moz-phab <using-moz-phab>`.

See also this `blog post
<https://smacleod.ca/posts/commit-series-with-phabricator/>`_ on
working with commit series in Phabricator.

We will be working on a solution to automate the submission and
updating of commit series.

****************
Applying Patches
****************

You can pull down the commits from any revision you have access with
this command::

    $ arc patch <revision id>

It is helpful to understand that ``arc patch``, by default, will not attempt to
patch the revision on top of your current working set. Instead, it applies the
changes on top of the same parent commit the author used and creates a new
commit and a new branch (git) or bookmark (hg). If it cannot find the same
parent commit in your local repo then it will warn you and give you the option
to apply it on top of the current working set. If you wish to test a revision
on top of your current working set use ``arc patch --nobranch``.

If you have a stack of revisions (see above section
:ref:`series-of-commits`), the commits from all previous revisions
will be applied as well.  Note that if you are pulling down a stack of
revisions but have a different commit currently checked out than was
used as the parent of the first commit, you will get warnings like
this:

.. code-block:: text

    This diff is against commit a237e16c2f716f55a22d53279f3914a231ae4051, but
    the commit is nowhere in the working copy. Try to apply it against the
    current working copy state? (.) [Y/n]

This is because the first commit now has a different parent and hence
a different SHA.  You can avoid this problem by updating to the parent
of the first commit before running ``arc patch``.
