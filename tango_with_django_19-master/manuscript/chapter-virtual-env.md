#Virtual Environments {#chapter-virtual-environments}
Virtual environments allow multiple installations of Python and their relevant
packages to exist in harmony. This is the generally accepted approach to
configuring a Python setup nowadays.

They are pretty easy to setup. Assuming you have `pip` installed, you can install the following packages:

{lang="text",linenos=off}   
	$ pip install virtualenv
	$ pip install virtualenvwrapper


The first package provides you with the infrastructure to create a
virtual environment. See [a non-magical introduction to Pip and
Virtualenv for Python
Beginners](http://dabapps.com/blog/introduction-to-pip-and-virtualenv-python/)
by Jamie Matthews for details about using `virtualenv`. However, using
just *virtualenv* alone is rather complex. The second package provides a
wrapper to the functionality in the `virtualenv` package and makes life a
lot easier. The wrapper
provides a series of extensions by [Doug
Hellman](http://doughellmann.com/) to the original `virtualenv` tool,
making it easier for us to create, delete and use virtual environments.

If you are using a linux/unix based OS, then to use the wrapper you need
to call the following shell script from your command line:

{lang="text",linenos=off}
	$ source virtualenvwrapper.sh

It is a good idea to add this to your bash/profile script. You therefore don't
have to run it each and every time you want to use a virtual environment. However, if you are using windows, then install the
[virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win)
package:

{lang="text",linenos=off}
	$ pip install virtualenvwrapper-win

Now you should be all set to create a virtual environment:

{lang="text",linenos=off}
	$ mkvirtualenv rango

You can list the virtual environments created with `lsvirtualenv`, and
you can activate a virtual environment as follows:

{lang="text",linenos=off}
	$ workon rango
	(rango)$

Your prompt with change and the current virtual environment will be
displayed, i.e. rango. Now within this environment you will be able to
install all the packages you like, without interfering with your
standard or other environments. Try `pip list` to see you don't have
`Django` or `Pillow` installed in your virtual environment. You can now
install them with `pip` so that they exist in your virtual environment.

In our [chapter on deployment](#chapter-deploy), we will go through a similar process when deploying your application to [PythonAnywhere](https://www.pythonanywhere.com/?affiliate_id=000116e3).

