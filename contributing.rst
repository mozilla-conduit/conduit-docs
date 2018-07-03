#######################
Contributing to Conduit
#######################

******************
General Guidelines
******************

We appreciate any contributions to the applications that make up the
Conduit system.  There are some common tools, processes, and
guidelines that most of the Conduit apps follow.  Each application
also has specific setup instructions; see the individual
:ref:`conduit-repos`.

We've created the `Suite <https://github.com/mozilla-conduit/suite>`_ project
to simplify the integration of all containers within the developer's
machine.

Bugs
----

We use `Bugzilla <https://bugzilla.mozilla.org>`_ for bug tracking,
even for those repos hosted on GitHub.  Although Bugzilla is a
heavier-weight tool than GitHub issues, it provides us with better
tracking and coordination, along with support for security bugs and
other confidential information.  Most bugs belong in the `Conduit
product
<https://bugzilla.mozilla.org/describecomponents.cgi?product=Conduit>`_,
with the exception of the `PhabBugz BMO extension
<https://bugzilla.mozilla.org/describecomponents.cgi?product=bugzilla.mozilla.org&component=Extensions%3A%20PhabBugz#Extensions%3A%20PhabBugz>`_.

Code Review
-----------

We use our `Phabricator instance
<https://phabricator.services.mozilla.com>`_ for code review, even for
those repos hosted on GitHub.  It is tied to our Bugzilla instance for
both identity and issue management.  See the :doc:`phabricator-user`
for more information.

.. note:: Please test your code before creating a revision in Phabricator.

Technologies
------------

We have a wiki page detailing the `tech stack
<https://wiki.mozilla.org/EngineeringProductivity/Projects/Conduit/Tech_Stack>`_
we have chosen.  Although it is, and will always be, a work in
progress, it lists both our chosen technologies and reasons behind
them.  New Conduit applications are expected to follow these
guidelines unless there is good reason to deviate, which should be
discussed with the Conduit development team.

.. _conduit-repos:

********************
Conduit Repositories
********************

The source code for most Conduit applications lives on GitHub.

* `lando-api <https://github.com/mozilla-conduit/lando-api>`_ has the
  main logic of the custom automatic-landing system that has been
  integrated with our Phabricator instance.

* `lando-ui <https://github.com/mozilla-conduit/lando-ui>`_ is a
  separate web application that is the main graphical user interface
  to lando-api.

* `PhabBugz
  <https://github.com/mozilla-bteam/bmo/tree/master/extensions/PhabBugz>`_,
  the BMO extension that maps BMO security policy to Phabriator and
  other such integrations, is a directory within the monolithic `BMO
  repo <https://github.com/mozilla-bteam/bmo>`_.  As with the rest of
  BMO, it is written in `Perl <https://www.perl.org>`_.

* `phabricator-extensions
  <https://github.com/mozilla-services/phabricator-extensions>`_
  contains our Conduit extensions to Phabricator, which mainly relate
  to integration with BMO.  As with Phabricator itself, these are
  written in `PHP <https://php.net>`_.

* `mozphab <https://github.com/mozilla-services/mozphab>`_ contains
  the deployment scripts and configuration for our Phabricator
  installation.  The files are a mixture of Python, PHP, shell
  scripts, and config files.

* `bmo-extensions
  <https://github.com/mozilla-conduit/bmo-extensions>`_ is a
  docker-based development environment for our Bugzilla-Phabricator
  integration pieces.

* `conduit-docs <https://github.com/mozilla-conduit/conduit-docs>`_
  contains the source for the docs you are reading now.

* `autoland-transplant <https://github.com/mozilla-conduit/autoland-transplant>`_
  is a tool that automatically lands patches from one Mercurial tree to
  another.

* `suite <https://github.com/mozilla-conduit/suite>`_
  allows you to connect and run all above services in a local development
  environment.
