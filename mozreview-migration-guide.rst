#######################################
Migrating from MozReview to Phabricator
#######################################

*************************************************
Key differences between MozReview and Phabricator
*************************************************

**MozReview**

- Most of the interfacing with the review tool is done by the ``hg`` command.
- Commits are updated in-place with ``hg amend``, histedit, etc.
- When landing, the commit messages appear the same as you authored them, with the list of reviewers rewritten to reflect approvals.
- Patches in a series all land at the same time.

**Phabricator**

- Most of the interfacing with the review tool is done by the ``arc`` command.
- You choose how commits are updated.  Phabricator supports both MozReview-style amended commits or GitHub-style fixup commits.
- When landing, the commit message is copied from your Phabricator review summary.
- Patches in a series can land at different times.

****************
Common Questions
****************

.. contents:: :local:

What will happen to my active code reviews?
-------------------------------------------

MozReview will stop accepting new code reviews 2 weeks before it is taken offline.  During that period you will have time to finish your in-flight reviews.

Authors must manually migrate their reviews to Phabricator if they still have unfinished reviews at the end of the 2 week shutdown notice period.  Join us in **#phabricator** on IRC or Slack if you need assistance with this.


What will happen to the patches MozReview contains today?
---------------------------------------------------------

All of the patches in MozReview will be preserved.  All of the links to MozReview patches in Bugzilla will continue to work.

The links in Bugzilla will change during the migration.  Instead of linking to MozReview reviews, Bugzilla will link to raw patches in unified-diff format.  A snapshot of the review repository is available for advanced users. See :ref:`how-to-apply-patches`.


I like editing a series of commits in-place before landing them.  Can I still do that?
--------------------------------------------------------------------------------------

Yes.  Phabricator supports the Mercurial workflow we have today, where review feedback is amended to the commit you originally submitted for reviews.  See the :doc:`phabricator-user` for details.

The amended-commit workflow is easy to use with Git, too.


I like the GitHub workflow of fixup commits that are squashed during landing.  Can I do that?
---------------------------------------------------------------------------------------------

Yes.  Phabricator has support for the GitHub-style squash-on-merge workflow. See our :doc:`phabricator-user` for details.


How do I run Try builds?
------------------------

Try builds need to be run from the command line.  Adding the ability to trigger Try builds from the Lando UI is a priority for us.


Can I chain related reviews together in Phabricator like I did in MozReview?
----------------------------------------------------------------------------

Yes.  Related reviews in Phabricator, called “stacks”, are also more flexible than reviews in MozReview.

In MozReview, all reviews in a series of commits must be approved before any one review can land.  All of the commits in the series land together.

In Phabricator, code reviews can be stacked however the author wishes, with a change depending on one or more other reviews.  You can land the reviews that are lowest in the stack while still taking feedback on the reviews higher up.  This is great for, say, landing a refactoring or bugfix before landing a feature that builds on top of it.

Our :doc:`phabricator-user` has instructions for using stacks.


Can I use ‘hg push’ to create and update reviews?
-------------------------------------------------

Not at this time.  We have created prototypes to see how this could work. This may be developed in the future.


.. _how-to-apply-patches:

How do I apply patches from old code reviews to my source tree after MozReview has shut down?
---------------------------------------------------------------------------------------------

#. Visit the bug associated with the review you want to reconstruct.
#. Click on the “MozReview Requests” section.
#. Click on the link for the review you want to get patches for. You will be taken to the MozReview patch archive for that revision.
#. Copy the link to the diff you want to download.
#. Import the diff with ``hg import --no-commit --exact https://mozreview-archive.s3-website.us-east-2.amazonaws.com/12345/r12345-diff[SOME-VERSION].patch``

There is also a snapshot of the review repo available for more advanced users.
