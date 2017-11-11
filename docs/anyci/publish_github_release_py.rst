``publish_github_release.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add-on automating the creation of GitHub releases.

Based on the git branch found in the current working directory, it allows to
automatically create a GitHub ``prerelease`` and/or ``release`` and upload
associated packages.

Getting Started
"""""""""""""""

To create a pre-release named ``latest``::

    ci_addons publish_github_release --prerelease-packages "dist/*"

To create a release named after the current tag::

    ci_addons publish_github_release --release-packages "dist/*"


In both case, packages found in *dist* directory are uploaded.


.. note::

    Pre-releases are created only if the current commit is *NOT* a tag (``latest`` tag is automatically
    ignored). Similarly, releases are created *ONLY* if current commit is a tag (different from ``latest``).


Terminology
"""""""""""

**Prerelease**: By default, this corresponds to a GitHub prerelease associated with a tag named
``latest`` and named ``Latest (updated on YYYY-MM-DD HH:MM UTC)``. The prerelease is automatically
updated each time the ``publish_github_release`` script is executed. Updating the ``latest``
prerelease means that (1) the latest tag is updated to point to the current HEAD, (2) the name is
updated and (3) latest packages are uploaded to replace the previous ones. GitHub prerelease are
basically release with *draft* option set to False and *prerelease* option set to True.

**Release**: This corresponds to a GitHub release automatically created by ``publish_github_release``
script only if it found that HEAD was associated with a tag different from ``latest``. It has both
*draft* and *prerelease* options set to False. Once packages have been associated with such a release,
they are not expected to be removed.

Usage
"""""

::

    ci_addons publish_github_release [-h]
                                     [--release-packages [PATTERN [PATTERN ...]]]
                                     [--prerelease-packages [PATTERN [PATTERN ...]]]
                                     [--prerelease-packages-clear-pattern PATTERN]
                                     [--prerelease-packages-keep-pattern PATTERN]
                                     [--prerelease-tag PRERELEASE_TAG]
                                     [--prerelease-name PRERELEASE_NAME]
                                     [--prerelease-sha PRERELEASE_SHA]
                                     [--token GITHUB_TOKEN]
                                     [--exit-success-if-missing-token]
                                     [--re-upload]
                                     [--display-python-wheel-platform]
                                     [--dry-run]
                                     ORG/PROJECT

.. note::

    - Packages to upload can be a list of paths or a list of globbing patterns.


Mini-language for packages selection
""""""""""""""""""""""""""""""""""""

To facilitate selection of specific packages, if any of the strings described below are
found in arguments associated with with either ``--prerelease-packages``
or ``--release-packages``, they will be replaced.

**<PYTHON_WHEEL_PLATFORM>**: This string is replaced by the current
platform as found in python wheel package names (e.g manylinux1, macosx, or win).
Executing ``ci_addons publish_github_release --display-python-wheel-platform``
returns the same string.

**<COMMIT_DATE>**: This string is replaced by the YYYYMMDD date
as returned by ``git show -s --format="%ci"``.

**<COMMIT_SHORT_SHA>**: This string is replaced by the sha
as returned by ``git rev-parse --short=7 HEAD``.

**<COMMIT_DISTANCE>**: This string is replaced by the distance
to the tag specified using ``--prerelease-tag``. If the tag does not exist,
it corresponds to the number of commits. This is particularly useful when
selecting prerelease packages generated using `pep440-pre style <https://github.com/warner/python-versioneer/blob/master/details.md#how-do-i-select-a-version-style>`_
implemented in `python-versioneer`.


Use case: Automatic upload of release packages associated with a tag
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

In this example, the script automatically detects that the current branch
HEAD is associated with the tag **1.0.0** and automatically uploads all
packages found in the ``dist`` directory.

::

    $ cd PROJECT

    $ git describe
    1.0.0

    $ ci_addons publish_github_release ORG/PROJECT \
      --release-packages "dist/*"
    Checking if HEAD is a release tag
    Checking if HEAD is a release tag - yes (found 1.0.0: creating release)

    created '1.0.0' release
      Tag name      : 1.0.0
      ID            : 5436107
      Created       : 2017-02-13T06:36:29Z
      URL           : https://github.com/ORG/PROJECT/releases/tag/1.0.0
      Author        : USERNAME
      Is published  : True
      Is prerelease : False

    uploading '1.0.0' release asset(s) (found 2):
      uploading dist/sandbox-1.0.0-cp27-cp27m-manylinux1.whl
      download_url: https://github.com/ORG/PROJECT/releases/download/1.0.0/sandbox-1.0.0-cp27-cp27m-manylinux1.whl

      uploading dist/sandbox-1.0.0-cp35-cp35m-manylinux1.whl
      download_url: https://github.com/ORG/PROJECT/releases/download/1.0.0/sandbox-1.0.0-cp35-cp35m-manylinux1.whl

Use case: Automatic creation of "nightly" prerelease from different build machines
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

When building projects using continuous integration services (e.g Appveyor,
TravicCI, or CircleCI), the *publish_github_release* script has the following
responsibilities:

* update the nightly tag reference
* update the release name
* keep only the most recent packages. This means that after successfully
  uploading package generating on a given platform, the older ones will be
  removed.

To fulfill its requirements, *publish_github_release* provides two
convenient options ``--prerelease-packages-clear-pattern`` and ``--prerelease-packages-keep-pattern``.

**prerelease-packages-clear-pattern**: This option allows to select all packages
that should be removed from the prerelease. For example, on a machine responsible
to generate windows python wheels, the following pattern can be used :``"*win*.whl"``.

**prerelease-packages-keep-pattern**: This option allows to keep packages
that have been selected by the previous globbing pattern. For example, assuming
development package names contain the date of the commit they are built from,
specifying a globbing pattern with the date allows to delete older packages while
keeping only the new ones built from that commit.

In the following example, we assume a prerelease done on 2017-02-12 with
16 packages (4 linux, 4 macosx, and 8 windows) already exists. The command
reported below corresponds to the execution of the script on a linux machine,
after one additional commit has been done the next day.

::

  $ cd PROJECT

  $ git describe
  1.0.0-2-g9d40177

  $ commit_date=$(git log -1 --format="%ad" --date=local | date +%Y%m%d)
  $ echo $commit_date
  20170213

  $ ci_addons publish_github_release ORG/PROJECT \
    --prerelease-packages dist/*.dev${commit_date}*manylinux1*.whl \
    --prerelease-packages-clear-pattern "*manylinux1*.whl" \
    --prerelease-packages-keep-pattern "*.dev${commit_date}*.whl"
  Checking if HEAD is a release tag
  Checking if HEAD is a release tag - no (creating prerelease)

  release nightly: already exists

  uploading 'nightly' release asset(s) (found 4):
    uploading dist/sandbox-1.0.0.dev20170213-cp27-cp27m-manylinux1_x86_64.whl
    download_url: https://github.com/ORG/PROJECT/releases/download/nightly/sandbox-1.0.0.dev20170213-cp27-cp27m-manylinux1_x86_64.whl

    uploading dist/sandbox-1.0.0.dev20170213-cp34-cp34m-manylinux1_x86_64.whl
    download_url: https://github.com/ORG/PROJECT/releases/download/nightly/sandbox-1.0.0.dev20170213-cp34-cp34m-manylinux1_x86_64.whl

    uploading dist/sandbox-1.0.0.dev20170213-cp35-cp35m-manylinux1_x86_64.whl
    download_url: https://github.com/ORG/PROJECT/releases/download/nightly/sandbox-1.0.0.dev20170213-cp35-cp35m-manylinux1_x86_64.whl

    uploading dist/sandbox-1.0.0.dev20170213-cp36-cp36m-manylinux1_x86_64.whl
    download_url: https://github.com/ORG/PROJECT/releases/download/nightly/sandbox-1.0.0.dev20170213-cp36-cp36m-manylinux1_x86_64.whl

  deleting 'nightly' release asset(s) (matched: 8, matched-but-keep: 4, not-matched: 12):
    deleting sandbox-1.0.0.dev20170212-cp27-cp27m-manylinux1_x86_64.whl
    deleting sandbox-1.0.0.dev20170212-cp34-cp34m-manylinux1_x86_64.whl
    deleting sandbox-1.0.0.dev20170212-cp35-cp35m-manylinux1_x86_64.whl
    deleting sandbox-1.0.0.dev20170212-cp36-cp36m-manylinux1_x86_64.whl
    nothing to delete

  resolved 'master' to '9d40177e6d3a69890de8ea359de2d02a943d2e10'
  updating 'nightly' release:
    target_commitish: '62fe605938ff252e4ddee05b5209299a1aa9a39e' -> '9d40177e6d3a69890de8ea359de2d02a943d2e10'
    tag_name: 'nightly' -> 'nightly-tmp'

  deleting reference refs/tags/nightly
  updating 'nightly-tmp' release:
    tag_name: 'nightly-tmp' -> 'nightly'

  deleting reference refs/tags/nightly-tmp
  updating 'nightly' release:
    target_commitish: '62fe605938ff252e4ddee05b5209299a1aa9a39e' -> '9d40177e6d3a69890de8ea359de2d02a943d2e10'

Use case: Automatic creation of GitHub releases and prereleases
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This can be done by combining the options ``--release-packages``
and ``--prerelease-packages``.

Note also the use of ``--display-python-wheel-platform`` to automatically
get the current python platform.

For example::

  $ commit_date=$(git log -1 --format="%ad" --date=local | date +%Y%m%d)

  $ platform=$(ci_addons publish_github_release ORG/PROJECT --display-python-wheel-platform)
  $ echo $platform
  manylinux1

  $ ci_addons publish_github_release ORG/PROJECT \
      --release-packages "dist/*" \
      --prerelease-packages dist/*.dev${commit_date}*${platform}*.whl \
      --prerelease-packages-clear-pattern "*${platform}*.whl" \
      --prerelease-packages-keep-pattern "*.dev${commit_date}*.whl"

The same can also be achieved across platform using the convenient mini-language for package
selection::

  $ ci_addons publish_github_release ORG/PROJECT \
      --release-packages "dist/*" \
      --prerelease-packages "dist/*.dev<COMMIT_DATE>*<PYTHON_WHEEL_PLATFORM>*.whl" \
      --prerelease-packages-clear-pattern "*<PYTHON_WHEEL_PLATFORM>*.whl" \
      --prerelease-packages-keep-pattern "*.dev<COMMIT_DATE>*.whl"

Testing
"""""""

Since the add-on tests interact with GitHub API, there are not included in the
regular scikit-ci-addons collection of tests executed using pytest. Instead,
they needs to be manually executed following these steps:

(1) Generate a `personal access token <https://github.com/settings/tokens/new>`_
    with at least ``public_repo`` scope enabled.
(2) Create a *test* project on GitHub with at least one commit.
(3) Check out sources of your *test* project.
(4) Create a virtual environment, download scikit-ci-addons source code, and install its requirements.
(5) Execute the test script.

For example::

  export GITHUB_TOKEN=...   # Change this with the token generated above in step (1)
  TEST_PROJECT=jcfr/sandbox # Change this with the project name created above in step (2)

  cd /tmp
  git clone https://github.com/scikit-build/scikit-ci-addons
  cd scikit-ci-addons/
  mkvirtualenv scikit-ci-addons-test
  pip install -r requirements.txt
  SRC_DIR=$(pwd)

  cd /tmp
  git clone https://github.com/$TEST_PROJECT test-project
  cd test-project

  python $SRC_DIR/anyci/tests/test_publish_github_release.py $TEST_PROJECT --no-interactive

