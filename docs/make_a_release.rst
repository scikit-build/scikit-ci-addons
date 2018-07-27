=====================
How to Make a Release
=====================

A core developer should use the following steps to create a release of
**scikit-ci-addons**.


1. Make sure that all CI tests are passing on `AppVeyor`_, `CircleCI`_ and `Travis CI`_.


2. List all tags sorted by version

  .. code::

    $ git tag -l | sort -V

3. Choose the next release version number

  .. code::

    $ release=X.Y.Z

  .. warning::

      To ensure the packages are uploaded on `PyPI`_, tags must match this regular
      expression: ``^[0-9]+(\.[0-9]+)*(\.post[0-9]+)?$``.


4. Download latest sources

  .. code::

    $ cd /tmp && \
      git clone git@github.com:scikit-build/scikit-ci-addons && \
      cd scikit-ci-addons

5. Tag the release

  .. code::

    $ git tag --sign -m "scikit-ci-addons ${release}" ${release} origin/master

  .. warning::

      This step requires a GPG signing key.


6. Create the source distribution and wheel

  .. code::

    $ python setup.py sdist bdist_wheel


7. Publish the release tag

  .. code::

    $ git push origin ${release}


8. After configuring `~/.pypirc <https://packaging.python.org/distributing/#uploading-your-project-to-pypi>`_,
   upload the distributions on `PyPI`_

  .. code::

    twine upload dist/*

  .. note::

    To first upload on `TestPyPI`_ , do the following::

        $ twine upload -r pypitest dist/*


9. Create a clean testing environment to test the installation

  .. code::

    $ mkvirtualenv scikit-ci-addons-${release}-install-test && \
      pip install scikit-ci-addons && \
      ci_addons --list && \
      ci_addons --version

  .. note::

    If the ``mkvirtualenv`` is not available, this means you do not have `virtualenvwrapper`_
    installed, in that case, you could either install it or directly use `virtualenv`_ or `venv`_.

    To install from `TestPyPI`_, do the following::

        $ pip install -i https://test.pypi.org/simple scikit-ci-addons


10. Cleanup

  .. code::

    $ deactivate  && \
      rm -rf dist/* && \
      rmvirtualenv scikit-ci-addons-${release}-install-test

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _virtualenv: http://virtualenv.readthedocs.io
.. _venv: https://docs.python.org/3/library/venv.html

.. _AppVeyor: https://ci.appveyor.com/project/scikit-build/scikit-ci-addons/history
.. _CircleCI: https://circleci.com/gh/scikit-build/scikit-ci-addons
.. _Travis CI: https://travis-ci.org/scikit-build/scikit-ci-addons/builds

.. _PyPI: https://pypi.org/project/scikit-ci-addons
.. _TestPyPI: https://test.pypi.org/project/scikit-ci-addons