######################
Phabricator at Mozilla
######################

**********
User Guide
**********

.. todo:: Replace links to Phabricator documentation with links to our
	  production Diviner site, when it's launched.

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

Creating an Account
===================

The first step toward submitting a patch via Phabricator is to create
an account.  Click the "Log In" button at the top of any Phabricator
page.

.. image:: images/login-button.png
   :align: center
   :alt: Screenshot of Phabricator login button

You'll be taken to another page with a single button, which will take
you to `bugzilla.mozilla.org <https://bugzilla.mozilla.org>`_ (BMO) to
log in or register a new account.

.. image:: images/bmo-login.png
   :align: center
   :alt: Screenshot of BMO login button

After you've done so, you'll be redirected back to Phabricator, where
you will be prompted to create a new Phabricator account.

.. image:: images/create-account.png
   :align: center
   :alt: Screenshot of account-creation form

The "Real Name" field is taken from your BMO account's real name.  If
your BMO real name also contains the ircnick convention, that is, a
username starting with a colon, it will be extracted and placed into
the Phabricator account's username field.  Note that if you surrounded
it with parentheses, brackets, or other punctuation, you may need to
strip that out of the Phabricator real name field as well.  Above is a
screenshot of the account-creation form for a BMO user with the real
name "Phabricator Test [:phabtest]".  Before clicking "Register
Account" the remaining "[]" should be deleted from the real name.
Note that the username field is mandatory, so if you didn't have one
automatically filled in, you'll have to pick one.

.. important::
   The username field is unique.  You should pick a clearly
   identifiable username, particularly if you will be doing code
   reviews, such as your nick on irc.mozilla.org.  If your nick is not
   available but you think it should be because, for example, you are
   at least somewhat known in the Mozilla community, please file a bug
   or let us know in #phabricator on irc.mozilla.org.

.. todo:: link to appropriate product & component above
.. todo:: are we really keeping 2FA on?

You now have a Phabricator account set up and can both submit and
review patches (along with using the other Phabriator applications).

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
applications and utilities:

* Dashboards allow users to set up custom pages to display useful
  information, for example assigned reviews.  It seems somewhat
  limited, though, so we'll evaluate how useful it really is.

* Pholio is an application for reviewing mock-ups and designs.
  Mozilla doesn't have a central application for this, so we'd like
  your input on whether Pholio is useful.

* Badges, macros, and tokens: These are mostly bits of whimsy that
  might enhance user experience by providing some levity.  If they're
  fun, or at least harmless, we'll leave them; if they become annoying
  or distracting, we may remove them.

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
