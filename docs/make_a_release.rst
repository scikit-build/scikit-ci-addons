.. _making_a_release:

================
Making a release
================

A core developer should use the following steps to create a release `X.Y.Z` of
**scikit-ci-addons** on `PyPI`_.

-------------
Prerequisites
-------------

* All CI tests are passing on `AppVeyor`_, `CircleCI`_ and `Travis CI`_.

* You have a `GPG signing key <https://help.github.com/articles/generating-a-new-gpg-key/>`_.

-------------------------
Documentation conventions
-------------------------

The commands reported below should be evaluated in the same terminal session.

Commands to evaluate starts with a dollar sign. For example::

  $ echo "Hello"
  Hello

means that ``echo "Hello"`` should be copied and evaluated in the terminal.

----------------------
Setting up environment
----------------------

1. First, `register for an account on PyPI <https://pypi.org>`_.


2. If not already the case, ask to be added as a ``Package Index Maintainer``.


3. Create a ``~/.pypirc`` file with your login credentials::

    [distutils]
    index-servers =
      pypi
      pypitest

    [pypi]
    username=<your-username>
    password=<your-password>

    [pypitest]
    repository=https://test.pypi.org/legacy/
    username=<your-username>
    password=<your-password>

  where ``<your-username>`` and ``<your-password>`` correspond to your PyPI account.


---------------------
`PyPI`_: Step-by-step
---------------------

1. Make sure that all CI tests are passing on `AppVeyor`_, `CircleCI`_ and `Travis CI`_.


2. Download the latest sources

  .. code::

    $ cd /tmp && \
      git clone git@github.com:scikit-build/scikit-ci-addons && \
      cd scikit-ci-addons


3. List all tags sorted by version

  .. code::

    $ git fetch --tags && \
      git tag -l | sort -V


4. Choose the next release version number

  .. code::

    $ release=X.Y.Z

  .. warning::

      To ensure the packages are uploaded on `PyPI`_, tags must match this regular
      expression: ``^[0-9]+(\.[0-9]+)*(\.post[0-9]+)?$``.


5. In `README.rst`, update `PyPI`_ download count after running `this big table query`_
   and commit the changes.

  .. code::

    $ git add README.rst && \
      git commit -m "README: Update download stats [ci skip]"

  ..  note::

    To learn more about `pypi-stats`, see `How to get PyPI download statistics <https://kirankoduru.github.io/python/pypi-stats.html>`_.

6. Tag the release

  .. code::

    $ git tag --sign -m "scikit-ci-addons ${release}" ${release} master

  .. warning::

      We recommend using a `GPG signing key <https://help.github.com/articles/generating-a-new-gpg-key/>`_
      to sign the tag.


7. Create the source distribution and wheel

  .. code::

    $ python setup.py sdist bdist_wheel


8. Publish the both release tag and the master branch

  .. code::

    $ git push origin ${release} && \
      git push origin master


9. Upload the distributions on `PyPI`_

  .. code::

    twine upload dist/*

  .. note::

    To first upload on `TestPyPI`_ , do the following::

        $ twine upload -r pypitest dist/*


10. Create a clean testing environment to test the installation

  .. code::

    $ mkvirtualenv scikit-ci-addons-${release}-install-test && \
      pip install scikit-ci-addons && \
      ci_addons --list && \
      ci_addons --version

  .. note::

    If the ``mkvirtualenv`` command is not available, this means you do not have `virtualenvwrapper`_
    installed, in that case, you could either install it or directly use `virtualenv`_ or `venv`_.

    To install from `TestPyPI`_, do the following::

        $ pip install -i https://test.pypi.org/simple scikit-ci-addons


11. Cleanup

  .. code::

    $ deactivate  && \
      rm -rf dist/* && \
      rmvirtualenv scikit-ci-addons-${release}-install-test


12. Add a ``Next Release`` section back in `CHANGES.rst`, commit and push local changes.

  .. code::

    $ git add CHANGES.rst && \
      git commit -m "CHANGES.rst: Add \"Next Release\" section [ci skip]" && \
      git push origin master


.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _virtualenv: http://virtualenv.readthedocs.io
.. _venv: https://docs.python.org/3/library/venv.html

.. _AppVeyor: https://ci.appveyor.com/project/scikit-build/scikit-ci-addons/history
.. _CircleCI: https://circleci.com/gh/scikit-build/scikit-ci-addons
.. _Travis CI: https://travis-ci.org/scikit-build/scikit-ci-addons/builds

.. _PyPI: https://pypi.org/project/scikit-ci-addons
.. _TestPyPI: https://test.pypi.org/project/scikit-ci-addons

.. _this big table query: https://bigquery.cloud.google.com/savedquery/280188050539:ce2c8d333d7d455aae8b76a7c0de7dae