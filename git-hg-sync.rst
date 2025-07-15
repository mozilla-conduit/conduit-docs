###########
Git Hg Sync
###########

While Lando now supports Git as a target SCM for landing, most automation
still relies pushes landing in `Mercurial <https://hg.mozilla.org/>`_. The `Git
Hg Sync component <https://github.com/mozilla-conduit/git-hg-sync/>`_ is in
charge of syncing commits and tags from GitHub to HgMO.


.. note:: `GitHub's Activity page <https://github.com/mozilla-firefox/firefox/activity>`_ looks similar to the PushLog. However it doesn't expose enough information for downstream use, nor does it provide for bespoke metadata and extension. Moreover, its `latency guarantees <https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-repository-events>`_ are not suited to our requirements in terms of delays and deliver guarantees.

It relies on logic from `git-cinnabar <https://github.com/glandium/git-cinnabar>`_ to create and record a two-way map between Git and Hg commits. Due to the difference in branch and tags management between Git and HgMO, changes to one Git repository may be reflected as changes to various repository in HgMO. More often, this depends on which git branch the commits were added.

************
Architecture
************

`git-hg-sync` is an event-driven component. It connects to Pulse, and subscribes to :ref:`notifications from Lando <pulse_notifications>`. At a high level, those notifications contain information about the source repository and branches that were modified, as well as tags to create.

.. mermaid::

   architecture-beta
     service lando(internet)[Lando]

     service github(database)[GitHub]
     service pulse(server)[Pulse]

     service sync(server)[Git Hg Sync]

     service hgmo(database)[HgMO]

     lando:B --> T:github
     lando:R --> L:pulse

     sync:L --> R:pulse
     sync:B --> R:github
     sync:R --> L:hgmo


After successfully having pushed changes to Git, Lando publishes messages to ``pulse.mozilla.org`` (AMQP). Those notifications contain information about the commits, branches and tags. Git-Hg-Sync processes those messages to determine what to fetch from Git and push to ``mercurial.mozilla.org`` (HgMO). It processes the notifications in strict order, retrying a failure until it succeeds (or is otherwise removed from the tip of the queue).

************************
Set-up and Configuration
************************

Git-Hg-Sync runs in GCPv2. This is configured in `the webservices-infra repository <https://github.com/mozilla/webservices-infra/tree/main/git-hg-sync>`_. This is a Docker-based deployment, following the `DockerFlow guidelines <https://github.com/mozilla-services/Dockerflow>`_. The images are `built in GitHub actions <https://github.com/mozilla-conduit/git-hg-sync/blob/main/.github/workflows/deploy.yml>`_.

The mapping of which data in Git should go where in Mercurial is described in a configuration file. For ease of maintenance, configuration files for all envirenments are checked in with the source code, and built into the Docker images. The configuration file to use in a specific deployment is selected based on the ``ENVIRONMENT`` variable. For example, the `production` environment will use the ``config-production.toml`` configuration.

There are three main sections in the configuration file: ``tracked_repositories``, ``branch_mappings``, and ``tag_mappings``.



Source Repositories
^^^^^^^^^^^^^^^^^^^

This is a list of repositories to monitor. The ``name`` is used for the working directory in the directory specified by ``clones.directory``.

.. note:: Any Pulse notification not related to a tracked repository will be ignored. The list is also used when bootstrapping the working directory, by pre-fetching the data in Git.


Branch Mapping
^^^^^^^^^^^^^^

The ``branch_mappings`` expresses which branches in Git should be synced to which individual repository in HgMO. There can be multiple matches for a single branch. It is possible to use regular expressions when matching branch names (as suggested by the name of the ``branch_pattern``). If a match is found, and the RE contained capturing groups, they can be reused to build the destination URL and branch.

::

  [[branch_mappings]]
  source_url = "https://github.com/mozilla-firefox/firefox.git"
  # esr<M> branches to mozilla-esr<M>
  branch_pattern = "^(esr\\d+)$"
  destination_url = "ssh://hg.mozilla.org/releases/mozilla-\\1/"
  destination_branch = "default"

.. note:: Backslashes need to be escaped to retain the special meaning in those regular expressions.

If the destination URL and branch names does *not* contain RE replacements, the bootstrap mechanism will also fetch data from the Mercurial remotes.

For large repositories such as Firefox, it can be useful to target ``mozilla-central`` in a branch mapping, even as a read-only source with impossible patterns. This is useful to benefit from Mercurial bundles (if available) to speed-up the initial import.

::

  #
  # MOZILLA-UNIFIED
  #
  # We don't sync to this repository, but we put it here first to fetch all
  # references early, with the benefit of bundles.
  #
  [[branch_mappings]]
  source_url = "https://github.com/mozilla-firefox/firefox.git"
  branch_pattern = "THIS_SHOULD_MATCH_NOTHING"
  destination_url = "https://hg.mozilla.org/mozilla-unified/"
  destination_branch = "NOT_A_VALID_BRANCH"

.. note:: As branch mappings are processed sequentially, such an entry needs to appear first for each source URL/branch mapping.


Tag Mapping
^^^^^^^^^^^

The ``tag_mappings`` is similar to the configuration for branches, including the support for regular expressions. Unlike branches, where Git commits are converted and pushed to Mercurial by git-cinnabar, it is necessary to recreate tags.

::

  [[tag_mappings]]
  source_url = "https://github.com/mozilla-firefox/firefox.git"
  # <M>_<m>(_<p>...)esr BUILD and RELEASE tags to mozilla-esr<M>
  tag_pattern = "^(FIREFOX|DEVEDITION|FIREFOX-ANDROID)_(\\d+)(_\\d+)+esr_(BUILD\\d+|RELEASE)$"
  destination_url = "ssh://hg.mozilla.org/releases/mozilla-esr\\2/"
  tags_destination_branch = "tags-unified"
  # Default
  #tag_message_suffix = "a=tagging CLOSED TREE DONTBUILD"

.. note:: The destination branch is named ``tags_destination_branch``.

Mercurial's support for tags relies on inspecting information from the ``.hgtags`` on the tip every branch. git-cinnabar therefore updates this file in the repository when creating new tags. However, he Git and Mercurial histories MUST remain in sync with a bijective mapping between each SCM. As a result is not possible update the ``.hgtags`` file in any of the branches receiving new code from Git.

The solution to this problem is to use a separate branch in Mercurial repositories, dedicated to receiving tags. The Git-Hg-Sync worker will maintain a Git branch named after ``tags_destination_branch`` *locally* in the working repository, and push that branch to a matching one in Mercurial.

.. note:: Tags branches are created as orphan branches without shared history with the ``default`` branch. The custom hook `SingleRootCheck <https://hg-edge.mozilla.org/hgcustom/version-control-tools/file/tip/hghooks/mozhghooks/check/single_root.py#l28>`_ in HgMO forbids branches with multiple roots. This hook must be disabled for any target repository.

Due to differences in the data models between Git and Mercurial, git-cinnabar refuses to create a tag which already exists in the repository, even if on a different branch. As a result, it is recommended to use the same ``tags_destination_branch`` for all ``tag_mappings`` with the same source from the ``tracked_repositories``.

.. warning:: As the work copy of the ``tags_destination_branch`` is only present in locally on the worker in Git. There might create bootstrapping issues if re-creating a work copy from scratch (see `bug 1962599 <https://bugzilla.mozilla.org/show_bug.cgi?id=1962599>`_ and `this comment <https://bugzilla.mozilla.org/show_bug.cgi?id=1973879#c4>`_). A manual fix would be to create the local ``tags_destination_branch`` from the Hg repo with the most recent updates to the tags.

The ``tags_mappings`` also has an optional ``tag_message_suffix``, which allows to specify a templated addition to the message of the commit creatining a tag. The default is shown commented out in the configuration snippet above.


Pulse (AMQP) Queue
^^^^^^^^^^^^^^^^^^

The configuration file can also contain details about Pulse, in the ``pulse`` section. Conventional parameters are written in the configuration file, but anything sensitive is left to be passed via environment. The rest of this section summarises the conventional parameters and their values.

.. warning:: Do not check Pulse credentials configuration in to Git.

.. note:: For more deployment flexibility, Pulse parameters are overridable via environment variables.

`Pulse <https://wiki.mozilla.org/Auto-tools/Projects/Pulse>`_ in an AMQP pub/sub service based on RabbitMQ. However, it enforces a handful of additional rules. Most importantly:

* exchanges should be named ``exchange/<clientId>/<name>``,
* they should be of type ``topic``, and
* queues should be name ``queue/<clientId>/<name>``.


In practice, service accounts are created using `PulseGuardian <https://pulseguardian.mozilla.org/>`_. Using those accounts, *Lando* is in charge of creating the exchange to which it publishes. Git Hg Sync, in turns, creates a queue, and binds it to the desired Lando exchange.

For the sake of sanity, the service accounts were created (manually) and named based on a regular pattern. For each environment ``ENV`` (``dev``, ``stage``, ``prod``), the users are ``lando<ENV>`` and ``githgsync<ENV>``. The ``name`` of the queue is simply ``pushes``. The routing key, while optional, is set to ``gitpushes``.

******************
Administrative CLI
******************

Git-Hg-Sync offers a small management interface via a command line tool available on the workers: ``git-hg-cli``. It requires a configuration file to be specified, and accepts a handful of commands.

::

   git-hg-cli -c <CONFIG> [config|dequeue|fetchrepo]

Inspecting the Run-time Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``config`` commands simply dumps a pretty-printed version of the live configuration to the console. This is a combination of the static information from the configuration file, as well as anything overriden from the environment.

Pre-fetching Working Directory Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``fetchrepo`` configuration is used to pre-populate or update the local working directory. It fetches all available commits from the Git source, as well as (optionally) any target Mercurial repo from the ``branch_mappings`` (as long as they do not contain dynamic replacement from regular expression capturing groups).

This command takes a mandatory ``--repository-url`` option, which should be the full URL of one of the ``tracked_repositries``.

If the ``--fetch-all`` option is passed, it data from Mercurial will also be fetched. The ``--verbose`` option requests that the output from the `git` and `hg` operation be output to the console.


Removing an Erroneous Pulse Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It may happen that a Pulse notification leads to a terminally failing action. As Git Hg Sync processes messages strictly in order, this means that any further processing is blocked. This would result in the symptom that HgMO (particularly ``autoland`` for Firefox) is no longer synced from Git.

.. warning:: Skipping a message may have unwanted consequences and require ad hoc fixes to be made to recover.

The ``dequeue`` command can be used to remove the tip message from the queue. For safety, it requires explicit passing of the ``--repository-url`` and ``--push-id`` options. The values of those options is compared to what is present in the first notification in the queue. Only iff those details matches will the message be removed.
