#############
Lando PushLog
#############

The unit of work on Mozilla codebases is a *Push*. A Push contains one or more
commits that have been pushed to the target repository by a given user in a
single event. The *PushLog* is an authoritative log of subsequent pushes.
Together with *Pulse notifications*, those are used to trigger downstream processing
such as CI (via TaskCluster), and to provide auditing capabilities. `The
PushLog was originally maintained by hg.mozilla.org
<https://mozilla-version-control-tools.readthedocs.io/en/latest/hgmo/pushlog.html>`_.
Since the Git migration, however, Lando maintains the PushLog as the source of
truth.

The Git PushLog retains the same format as the original one from HgMO for
backward compatibility and data retention. It also extends the data with new
Git-specific information. New and updated clients should be relying on the Git
information.

By default, new repositories in Lando will be created with PushLog support
enabled. However, it is possible to disable it on a per-repository basis. This
is useful for Mercurial repos, for which the HgMO pushlog is the source of
truth.

.. warning:: PushLog support is only partially implemented in Lando. No publicly accessible endpoint currently exists, and only `Pulse Notifications <pulse_notifications_>`_ are fully functional. See `bug 1940612 <https://bugzilla.mozilla.org/show_bug.cgi?id=1940612>`_.

*******
PushLog
*******

.. todo:

   lando list repos
   lando pushlog_view

************
JSON PushLog
************

.. todo::

  `/json-pushes`


  ``startID``, ``endID``
  ``full``
  ``commit``
  ``fromcommit``, ``tocommit``
  ``startdate``, ``enddate``
  ``version=3``
  Throw errors for ``version=1`` and ``version=2`` requests
  Throw errors for unversioned requests?


JSON Payload Formats
--------------------

Versions 1 and 2 were used for legacy HgMO Push logs. Version 3, described
below, is a variation of version 2, better suited to git.

Here::

  {
    "lastpushid": 21,
    "pushes": {
      "16": {
        "type": "git",
        "branch": "...",
        "commits": [
          "91826025c77c6a8e5711735adaa9766dd4eac7fc",
          "25f2a69ac7ac2919ef35c0b937b862fbb9e7e1f7"
        ],
        "date": 1227196396,
        "user": "user@example.com"
      }
    }
  }

The top-level objects contains the following properties:

``pushes``
   An object containing push information. See `Push Objects <push_objects_>`_ below.

``lastpushid``
   The push ID of the most recent push known to Lando.

   This value can be used by clients to determine if more pushes are
   available. For example, clients may query for N commits at a time
   by specifying ``endID``. The value in this property can tell these
   clients when they have exhausted all known pushes.

.. _push_objects:

Push Objects
^^^^^^^^^^^^

The value of each entry in the ``pushes`` object is an object describing
the push and the commits therein.

The following properties are always present:

``commits``
   An array of commit entries.

   By default, entries are 40 character commit SHA-1s included in the
   push. If ``full=1`` is specified, entries are objects containing
   commit metadata (see `Commit objects <commit_objects_>`_ below).

.. todo::

  ENFORCE THIS

   Commits are in DAG/revlog order with the tip-most commit last.

``date``
   Integer seconds since UNIX epoch that the push occurred.

   For pushes that take a very long time (more than a single second),
   the data will be recorded towards the end of the push, just before
   the transaction is committed to Mercurial. Although, this is an
   implementation detail.

   There is no guarantee of strict ordering between dates, i.e. the
   ``date`` of push ID ``N + 1`` could be less than the ``date`` of push
   ID ``N``. Such is how clocks work.

``user``
   The string username that performed the push.

.. _commit_objects:

Commit objects
^^^^^^^^^^^^^^

If ``full=1`` is specified, each entry in the ``commits`` array will be an
object instead of a string. Each object will have the following properties:

``commit``
   The 40 byte hex SHA-1 of the commit.

``parents``
   An array of 1 or 2 elements containing the 40 byte hex SHA-1 of the
   parent commit. Merges have 2 entries.

.. todo::

  CONFIRM THIS
   Root changesets have the
   value ``0000000000000000000000000000000000000000``.

``author``
   The author string from the changeset.

``desc``
   The changeset's commit message.

``branch``
   The branch the changeset belongs to.

``files``
   An array of filenames that were changed by this changeset.

Here's an example::

  {
    "author": "Eugen Sawin <esawin@mozilla.com>",
    "desc": "Bug 1110212 - Strong randomness for Android DNS resolver. r=sworkman",
    "files": [
      "other-licenses/android/res_init.c"
    ],
    "commit": "ee4fe2ec168e719e822dabcdd797c0cff9ce2407",
    "parents": [
      "803bc910c45a875d9d76dc689c45dd91a1e02e23"
    ]
  }



***************
PushLog webview
***************

.. todo::

  URL `/pushlog`

.. todo::

  Screenshot

.. _pulse_notifications:

*******************
Pulse notifications
*******************

Whenever a change has landed to a PushLog-enabled repository, Lando will send a Pulse notification.

A single message can represent any number of pushes to various `branches`. It may also contain any number of `tags`.

.. note:: For the purpose of syncing changes from Git to Mercurial, the `commit_id` in each in the `tags` object needs to exist in the target repository prior to the tag being created. It may be present in the `branches` object as part of the same message.

::

  {
    "type": "push",
    "repo_url": "https://lando.moz.tools/FIXME/firefox-autoland/pushlog",
    "branches": { "BRANCH": "commit_id", ...}
    "tags": { "TAG": "commit_id", ...}
    "time": 14609750810,
    "push_id": 120040,
    "user": "user@example.com",
    "push_json_url": "https://lando.moz.tools/FIXME/firefox-autoland/pushlog/json-pushes?version=2&startID=120039&endID=120040",
    "push_full_json_url": "https://lando.moz.tools/FIXME/firefox-autoland/pushlog/json-pushes?version=2&full=1&startID=120039&endID=120040"
  }


.. _creating_pulse_exchanges:

Creating Pulse Exchanges
------------------------

`Pulse <https://wiki.mozilla.org/Auto-tools/Projects/Pulse>`_ is an AMQP pub/sub service based on RabbitMQ. However, it enforces a handful of additional rules. Most importantly:

* exchanges should be named ``exchange/<clientId>/<name>``,
* they should be of type ``topic``, and
* queues should be name ``queue/<clientId>/<name>``.

In practice, service accounts are created using `PulseGuardian <https://pulseguardian.mozilla.org/>`_. Using those accounts, *Lando* is in charge of creating the exchange to which it publishes. :ref:`Git Hg Sync <config_pulse_queue>`, in turns, creates a queue, and binds it to the desired Lando exchange.

For the sake of sanity, the service accounts were created (manually) and named based on a regular pattern. For each environment ``ENV`` (``dev``, ``stage``, ``prod``), the users are ``lando<ENV>`` and ``githgsync<ENV>`` (e.g., ``landostage`` or ``githgsyncprod``). The ``name`` of the queue is simply ``pushes``. The routing key, while optional, is set to ``gitpushes``.

.. warning:: Do not check Pulse credentials configuration in to Git.

Lando will create the Exchange, if missing, when it first needs to publish to it. It could however be useful to create it ahead of time, as downstream consumers are not able to bind queues to an exchange until it exists. This can be done with the ``pulse_declare`` management command.

::

  $ lando pulse_declare
  Declared exchange exchange/landodev/pushes on <AMQP Connection: pulse.mozilla.org:5671// using <SSLTransport: 10.24.10.110:39608 -> 35.212.137.69:5671 at 0x7f891f864320> at 0x7f891f823150>

.. _pulse_notify:

Manually Sending Notifications
------------------------------

The ``lando`` management CLI has a ``pulse_notify`` command allowing to send a notification for a given repository (``--repository <REPO-NAME>``) and push (``--push_id <ID>``). The state of the PushLog for a target repository can be first inspected with a couple of other ancillary commands: ``list_repos`` and ``pushlog_view``.
 
::

  $ lando list_repos
  [...]
  ff-test-dev: https://github.com/mozilla-conduit/ff-test (git)
  $ lando pushlog_view --repository ff-test-dev --limit 1
  Push 180 in ff-test-dev@dev (git) (notified: False)
    Commit 02172852b4d274a8538e07fbd26e136c9c09607d in ff-test-dev@dev (git)
  $ lando pulse_notify --repository ff-test-dev -push_id 180
  Notifying for Push 180 in ff-test-dev@dev (git) ...
  {"EnvVersion": "2.0", "Fields": {"msg": "Sending {'payload': {'type': 'push', 'repo_url': 'https://github.com/mozilla-conduit/ff-test', 'branches': {'dev': '02172852b4d274a8538e07fbd26e136c9c09607d'}, 'tags': {}, 'time': '1750389650', 'push_id': 180, 'user': 'omehani@mozilla.com', 'push_json_url': 'FIXME', 'push_full_json_url': 'FIXME'}} ..."}, "Hostname": "lando-landingworkergit-0", "Logger": "lando", "Pid": 358542, "Severity": 6, "Timestamp": 1752544021423447296, "Type": "lando.pulse.pulse"}

By default, ``pulse_notify`` will refuse to send notifications for Pushes which (resp.)

1. have already been notified, or
2. are not the first un-notified Push.

Both those safeguards can be overridden with command line options (resp.)

1. ``--force-renotify``
2. ``--force-out-of-order``

.. warning:: There is a strong assumption that Pulse Notifications should only be delivered once. Re-sending notifications should be done carefully, and only when all implications of doing so are well understood. 

