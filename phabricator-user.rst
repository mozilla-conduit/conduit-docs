######################
Phabricator at Mozilla
######################

**********
User Guide
**********

As Mozilla's Phabricator instance has only small modifications from
stock Phabricator, most of those concerning integration points with
BMO (see various sections below), much of `Phabricator's user
documentation <https://secure.phabricator.com/book/phabricator/>`_
is fully applicable.

Arcanist is the command-line interface to Phabricator, mainly used to
submit patches for review.  There is an `Arcanist Quick Start guide
<https://secure.phabricator.com/book/phabricator/article/arcanist_quick_start/>`_,
a larger `Arcanist User Guide
<https://secure.phabricator.com/book/phabricator/article/arcanist/>`_,
and a specific `guide to "arc diff"
<https://secure.phabricator.com/book/phabricator/article/arcanist_diff/>`_
available in the main Phabricator documentation.  There are also other
related articles available under the `Application User Guides
<https://secure.phabricator.com/book/phabricator/>`_.

Differential is Phabricator's code-review tool.  Useful articles
include the `Differential User Guide
<https://secure.phabricator.com/book/phabricator/article/differential/>`_,
the `FAQ
<https://secure.phabricator.com/book/phabricator/article/differential_faq/>`_,
and the `Inline Comments guide
<https://secure.phabricator.com/book/phabricator/article/differential_inlines/>`_.
As usual, there are other articles available for specific subjects.

Another useful application is Herald, which can perform actions, such
as sending notifications, based on object changes (such as a
Differential revision being created or updated).  There is a short
`user guide
<https://secure.phabricator.com/book/phabricator/article/herald/>`_
available.

***********
Quick Start
***********

TBD

****************
Our Installation
****************

Mozilla's Phabricator instance is a stock installation, with a small patch
applied, and some custom extensions.  The patch and extensions are
intentionally small in scope and are limited to supporting integration
points with `bugzilla.mozilla.org <https://bugzilla.mozilla.org>`_
(henceforth referred to as "BMO").

We are using various GitHub repos for our code: the
`deployment scripts and config <https://github.com/mozilla-services/mozphab>`_ 
and our `patches and custom extensions
<https://github.com/mozilla-services/phabricator-extensions>`_.  There
is also a related `BMO extension
<https://github.com/mozilla-bteam/bmo/tree/master/extensions/PhabBugz>`_.

************
Applications
************

Phabricator is actually a suite of many applications, from a
code-review tool to wikis to a blogging platform.  At Mozilla, we
already have existing applications that solve many of these problems.
To prevent the re-emergence of the all-too-common problem of having to
choose between several tools that are all functionally similar, we
have disabled the use of some of these applications.

The default left-side menu in Phabricator lists the most important
applications for Mozilla's use case.  In addition to Differential and
Herald, described above, we support or are trialing several other
applications:

TBD

Note that Phabricator also has a post-commit review system called
Audit.  This application is mandatory, that is, it cannot be
disabled.  However, at the moment Mozilla has no processes for
post-commit review of Firefox and related code, so we do not recommend
its use, at least until such time as a process is deemed necessary and
implemented.  Audit may, of course, be useful to projects hosted on
the Mozilla Phabricator instance outside of Firefox.


***************
BMO Integration
***************

Since issue tracking and code review are tightly related, and since
BMO is currently the authority for identity and authorization around
both issue tracking and code review, including security and other
confidential bugs and fixes, our Phabricator instance is integrated
with BMO. This integration is intentionally lightweight in order
to limit customization of Phabricator, which has both maintenance and
opportunity costs, consisting of identity, authorization, links
between bugs and revisions, and basic review-status mirroring.

Identity
========

The main way to log into Phabricator is via BMO's auth delegation. A
user logging into Phabricator is taken to BMO to log in as usual and
will be redirected back to Phabricator if the login succeeds. If this
is the first time the user has logged into Phabricator, they will be
prompted to create an account. They can choose to use their BMO email
address or provide a new one, which will be separately verified. New
users will also be prompted to enter a separate username, unlike
BMO. This username will be used by Autoland to denote reviewers when
constructing the final commit message.

Authorization
=============

If a bug has one or more security groups applied to it, that is, it
has restricted visibility, any Differential revisions associated with
it are similarly restricted in visibility. This will initially only
apply to Firefox security groups, that is, groups with names matching
``*core-security*``. Any revision associated with a bug restricted via
other groups, e.g. infra, is visible only to the author and admins. We
can add proper support for such groups on request.

Links from Differential to BMO
==============================

A bug number must be entered when a patch is submitted to
Phabricator. This is stored in the revision metadata and provided in
the UI as a link to the associated bug on BMO.

Links from BMO to Differential
==============================

Upon the creation of a new revision in Differential, a stub
attachment, containing only the URL of the revision, is added to the
associated bug. Based on the attachment type, BMO automatically
redirects to Differential if the attachment link is clicked.

Review flags
============

For simplicity, and since Differential's review system does not map
cleanly to BMO's review flags, r+ flags, and only r+ flags, are set on
the stub attachment associated with a Differential revision when a
Phabricator user performs an "Accept Revision" action. The flag is
removed if the reviewer later issues a "Request Changes" or a "Resign
as Reviewer" action. Similarly, all r+ flags are removed if the author
selects any of the "Plan Changes", "Request Review", or "Abandon
Revision" actions. In the last case, the stub attachment is also be
obsoleted.
