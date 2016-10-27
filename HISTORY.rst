.. :changelog:

History
-------

scikit-ci-addons was initially developed in May 2016 by Omar Padron to facilitate
the continuous integration of the scikit-build project.

At that time, it consisted of code directly embedded in the CI script used in
scikit-build project.

Then, in early September 2016, with the desire to setup cross-platform continuous
integration for other project and avoid duplication or maintenance hell, the code
was factored out by Jean-Christophe Fillion-Robin into a set of reusable scripts
available in the scikit-ci project. By simply cloning the repository, it was
possible to more easily enable CI for other projects.

While this was an improvement, this prevented the distribution of standalone
and simple scikit-ci package. To better separate concerns and facilitate
testing and maintenance, in late September 2016, the scripts were moved into
their own project and scikit-ci-addons was born.

Finally, in late October 2016, Jean-Christophe came up with the concept of
scikit-ci-addons command line tool allowing to execute the scripts (or add-ons)
distributed within the scikit-ci-addons package.
