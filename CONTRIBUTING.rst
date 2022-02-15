============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Types of Contributions
----------------------

You can contribute in many ways:

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/scikit-build/scikit-ci-addons/issues.

If you are reporting a bug, please include:

* Any details about your CI setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

The scikit-ci-addons project could always use more documentation. We welcome help
with the official scikit-ci-addons docs, in docstrings, or even on blog posts and
articles for the web.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/scikit-build/scikit-ci-addons/issues.

If you are proposing a new feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Get Started
-----------

Ready to contribute? Here's how to set up `scikit-ci-addons` for local development.

1. Fork the `scikit-ci-addons` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/scikit-ci-addons.git

3. Install your local copy into a virtualenv. Assuming you have
   virtualenvwrapper installed (`pip install virtualenvwrapper`), this is how
   you set up your cloned fork for local development::

    $ mkvirtualenv scikit-ci-addons
    $ cd scikit-ci-addons/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and
   the tests, including testing other Python versions with tox::

    $ flake8
    $ python setup.py test
    $ tox

   If needed, you can get flake8 and tox by using `pip install` to install
   them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in `README.rst`.

3. The pull request should work for Python 2.7, and 3.x and all associated
   checks should pass.
