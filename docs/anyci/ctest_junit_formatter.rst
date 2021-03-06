``ctest_junit_formatter``
^^^^^^^^^^^^^^^^^^^^^^^^^

Add-on converting test results from CTest to JUnit format.

The add-on get the name of the latest build tag by reading the
first line of <BUILD_DIR>/Testing/TAG, and then convert the
file <BUILD_DIR>/Testing/<LATEST_TAG>/Test.xml. The conversion
results is outputted on stdout.

This add-on supports both Python 2 and Python 3 and is based on
`stackoverlow answer <http://stackoverflow.com/questions/6329215/how-to-get-ctest-results-in-hudson-jenkins#6329217>`_
contributed by `Calvin1602 <http://stackoverflow.com/users/124038/calvin1602>`_
and `MOnsDaR <http://stackoverflow.com/users/199513/monsdar>`_.

Usage::

    ci_addons ctest_junit_formatter BUILD_DIR > JUnit.xml

Example of use from CircleCI::

    $ mkdir ${CIRCLE_TEST_REPORTS}/CTest
    $ ci_addons ctest_junit_formatter BUILD_DIR > ${CIRCLE_TEST_REPORTS}/CTest/JUnit-${CIRCLE_NODE_INDEX}.xml

.. note::

    CircleCI will automatically aggregate test results generated by
    different node.

Example of CircleCI test summary with failing tests:

.. image:: /images/ctest_junit_formatter_circleci_example.png