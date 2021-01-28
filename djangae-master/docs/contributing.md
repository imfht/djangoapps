# Contributing to Djangae

Djangae is actively developed and maintained, so if you're thinking of contributing to the codebase, here is how to get started.

## Get started with development

1. First off, head to [our Github page](https://github.com/potatolondon/djangae) and fork the repository to have your own copy of it.
2. Clone it locally to start setting up your development environment
3. Run all tests to make sure your local version is working: `./runtests.sh`. This will also install all necessary dependencies.

## Pick an issue & send a pull request

If you spotted a bug in Djangae that you want to fix, it's a good idea to start
off by [adding an issue](https://github.com/potatolondon/djangae/issues/new).
This will allow us to verify that your issue is valid, and suggest ideas for fixing it, so
no time is wasted for you.

For help with creating the pull request, check out [Github documentation](https://help.github.com/articles/creating-a-pull-request/).

## Code style

Code style should follow PEP-8 with a loose line length of 100 characters.

## Need help?

Reach out to us on [djangae-users](https://groups.google.com/forum/#!forum/djangae-users) mailing list.

## Pull request requirements

For pull request to be merged, following requirements should be met:

- Tests covering new or changed code are added or updated
- Relevant documentation should be updated or added
- Line item should be added to CHANGELOG.md, unless change is really irrelevant

## Running tests

For running the tests, you just need to run:

    $ ./runtests.sh

On the first run this will download the App Engine SDK, pip install a bunch of stuff locally (into a folder, no virtualenv needed), download the Django tests and run them.  Subsequent runs will just run the tests. If you want to run the tests on a specific Django version, simply do:

    $ DJANGO_VERSION=1.8 ./runtests.sh

Currently the default is 1.8. TravisCI runs on 1.8 and 1.9 currently.

You can run specific tests in the usual way by doing:

    ./runtests.sh some_app.SomeTestCase.some_test_method
