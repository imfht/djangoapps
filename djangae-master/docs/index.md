# Djangae 2

**The best way to run Django on Google App Engine.**

Djangae (jan-gee) is a Django app that allows you to run Django applications on Google App Engine.

Google Group: [https://groups.google.com/forum/#!forum/djangae-users](https://groups.google.com/forum/#!forum/djangae-users)

Website: [https://djangae.org](https://djangae.org)

GitHub: [https://github.com/potatolondon/djangae](https://github.com/potatolondon/djangae)

Gitter: [https://gitter.im/potatolondon/djangae](https://gitter.im/potatolondon/djangae)

**Note: Djangae is under heavy development, stability is not guaranteed. A 2.0 release will happen when it's ready. If you are looking to use Djangae on Python 2, then take a look at the 1.x branch**

## Features

* Hooks to manage a series of Google Cloud emulators to simulate the Google App Engine environment locally
* A tasks app which implements "deferred" tasks on Google Cloud Tasks, and functions for iterating large datasets
* Utility functions to discover information about the running environment
* A series of security patches and checks to improve the security of your project
* Test utils for testing code that uses the Cloud Tasks API
* Apps for cross-request locking and efficient pagination on the Google Cloud Datastore

## Supported Django Versions

Djangae currently supports Django 2.2.

