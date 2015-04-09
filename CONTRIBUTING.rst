============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Bug reports
===========

When `reporting a bug <https://github.com/Debith/py3traits/issues>`_ please include:

    * Your operating system name, version and python version.
    * Failing test case created similar manner as in py3traits/examples.

Documentation improvements
==========================

py3traits could always use more documentation, whether as part of the
official py3traits docs, in docstrings, or even on the web in blog posts,
articles, and such.

Feature requests and feedback
=============================

The best way to send feedback is to file an issue at https://github.com/Debith/py3traits/issues.

If you are proposing a feature:

* Explain in detail how it would work or even better, create a failing test case similar manner as in py3traits/examples
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

Development
===========

To set up `py3traits` for local development:

1. `Fork py3traits on GitHub <https://github.com/Debith/py3traits/fork>`_.
2. Clone your fork locally::

    git clone git@github.com:your_name_here/py3traits.git

3. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. When you're done making changes, run all the checks, doc builder and spell checker with `tox <http://tox.readthedocs.org/en/latest/install.html>`_ one command::

    tox

5. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run ``tox``) [1]_.
2. Update documentation when there's new API, functionality etc. 
3. Add a note to ``CHANGELOG.rst`` about the changes.
4. Add yourself to ``AUTHORS.rst``.

.. [1] If you don't have all the necessary python versions available locally you can rely on Travis - it will 
       `run the tests <https://travis-ci.org/Debith/py3traits/pull_requests>`_ for each change you add in the pull request.
       
       It will be slower though ...
       
Tips
----

To run a subset of tests::

    tox -e envname -- py.test -k test_myfeature

To run all the test environments in *parallel* (you need to ``pip install detox``)::

    detox