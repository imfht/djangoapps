#Setting up your System {#chapter-system-setup}
This chapter provides a brief overview of the different components that you need to have working in order to develop Django apps.

I> ### Choosing a Python Version
I> Django supports both the Python 2.7.x and 3 programming languages. While they both share the same name, they are fundamentally different programming languages. In this chapter, we assume you are setting up Python 2.7.5 - you can change the version number as you require.

## Installing Python {#section-system-setup-python}
So, how do you go about installing Python 2.7/3.4 on your computer? You may already have Python installed on your computer - and if you are using a Linux distribution or OS X, you will definitely have it installed. Some of your operating system's functionality [is implemented in Python](http://en.wikipedia.org/wiki/Yellowdog_Updater,_Modified), hence the need for an interpreter!

Unfortunately, nearly all modern operating systems utilise a version of Python that is older than what we require for this tutorial. There's many different ways in which you can install Python, and many of them are sadly rather tricky to accomplish. We demonstrate the most commonly used approaches, and provide links to additional reading for more information.

W> ### Do not remove your default Python installation
W> This section will detail how to run Python 2.7.5 *alongside* your current Python installation. It is regarded as poor practice to remove your operating system's default Python installation and replace it with a newer version. Doing so could render aspects of your operating system's functionality broken!

### Apple mac OS/OS X
The most simple way to get Python 2.7.5 installed on your Mac is to download and run the simple installer provided on the official Python website. You can download the installer by visiting the webpage at <http://www.python.org/getit/releases/2.7.5/>.

I> ### Make sure you have the correct version for your Mac
I>
I> Ensure that you download the `.dmg` file that is relevant to your particular mac OS/OS X installation!

1.  Once you have downloaded the `.dmg` file, double-click it in the Finder.
2.  The file mounts as a separate disk and a new Finder window is presented to you.
3.  Double-click the file `Python.mpkg`. This will start the Python installer.
4.  Continue through the various screens to the point where you are ready to install the software. You may have to provide your password to confirm that you wish to install the software.
5.  Upon completion, close the installer and eject the Python disk. You can now delete the downloaded `.dmg` file.

You should now have an updated version of Python installed, ready for Django! Easy, huh? You can also install Python 3.4+ in a similar version, if you prefer to use Python 3.

### Linux Distributions
Unfortunately, there are many different ways in which you can download, install and run an updated version of Python on your Linux distribution. To make matters worse, methodologies vary from distribution to distribution. For example, the instructions for installing Python on [Fedora](http://fedoraproject.org/) may differ from those to install it on an [Ubuntu](http://www.ubuntu.com/) installation.

However, not all hope is lost. An awesome tool (or a *Python environment manager*) called [pythonbrew](https://github.com/utahta/pythonbrew) can help us address this difficulty. It provides an easy way to install and manage different versions of Python, meaning you can leave your operating system's default Python installation alone.

Taken from the instructions provided from [the pythonbrew GitHub page](https://github.com/utahta/pythonbrew) and [this Stack Overflow
question and answer page](http://stackoverflow.com/questions/5233536/python-2-7-on-ubuntu), the following steps will install Python 2.7.5 on your Linux distribution.

1.  Open a new terminal instance.
2.  Run the command `curl -kL http://xrl.us/pythonbrewinstall | bash`. This will download the installer and run it within your terminal for you. This installs pythonbrew into the directory `~/.pythonbrew`. Remember, the tilde (`~`) represents your home directory!
3.  You then need to edit the file `~/.bashrc`. In a text editor (such as `gedit`, `nano`, `vi` or `emacs`), add the following to a new line at the end of `~/.bashrc`: `[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc`
4.  Once you have saved the updated `~/.bashrc` file, close your terminal and open a new one. This allows the changes you make to take effect.
5.  Run the command `pythonbrew install 2.7.5` to install Python 2.7.5.
6.  You then have to *switch* Python 2.7.5 to the *active* Python installation. Do this by running the command `pythonbrew switch 2.7.5`.
7.  Python 2.7.5 should now be installed and ready to go.

T> ### Hidden Directories and Files
T> Directories and files beginning with a period or dot can be considered the equivalent of *hidden files* in Windows. [Dot files](http://en.wikipedia.org/wiki/Dot-file) are not normally visible to directory-browsing tools, and are commonly used for configuration files. You can use the `ls` command to view hidden files by adding the `-a` switch to the end of the command, giving the command `ls -a`.

### Windows {#section-system-setup-python-windows}
By default, Microsoft Windows comes with no installations of Python. This means that you do not have to worry about leaving existing versions be; installing from scratch should work just fine. You can download a 64-bit or 32-bit version of Python from [the official Python website](http://www.python.org/download/). If you aren't sure which one to download, you can determine if your computer is 32-bit or 64-bit by looking at the instructions provided [on the Microsoft website](http://windows.microsoft.com/en-gb/windows7/32-bit-and-64-bit-windows-frequently-asked-questions).

1.  When the installer is downloaded, open the file from the location to which you downloaded it.
2.  Follow the on-screen prompts to install Python.
3.  Close the installer once completed, and delete the downloaded file.

Once the installer is complete, you should have a working version of Python ready to go. By default, Python 2.7.5 is installed to the directory `C:\Python27`. We recommend that you leave the path as it is.

Upon the completion of the installation, open a Command Prompt and enter the command `python`. If you see the Python prompt, installation was successful. However, in certain circumstances, the installer may not set your Windows installation's `PATH` environment variable correctly. This will result in the `python` command not being found. Under Windows 7, you can rectify this by performing the following:

1.  Click the *Start* button, right click *My Computer* and select *Properties*.
2.  Click the *Advanced* tab.
3.  Click the *Environment Variables* button.
4.  In the *System variables* list, find the variable called *Path*, click it, then click the *Edit* button.
5.  At the end of the line, enter `;C:\python27;C:\python27\scripts`. Don't forget the semicolon - and certainly *do not* add a space.
6.  Click OK to save your changes in each window.
7.  Close any Command Prompt instances, open a new instance, and try run the `python` command again.

This should get your Python installation fully working. Things might [differ ever so slightly on Windows 10](http://stackoverflow.com/a/14224786).

## Setting Up the `PYTHONPATH`
With Python now installed, we now need to check that the installation was successful. To do this, we need to check that the `PYTHONPATH` [environment variable](http://en.wikipedia.org/wiki/Environment_variable) is setup correctly. `PYTHONPATH` provides the Python interpreter with the location of additional Python [packages and modules](http://stackoverflow.com/questions/7948494/whats-the-difference-between-a-python-module-and-a-python-package) which add extra functionality to the base Python installation. Without a correctly set `PYTHONPATH`, we'll be unable to install and use Django!

First, let's verify that our `PYTHONPATH` variable exists. Depending on the installation technique that you chose, this may or may not have been done for you. To do this on your UNIX-based operating system, issue the following command in a terminal.

{lang="text",linenos=off}
	$ echo $PYTHONPATH


On a Windows-based machine, open a Command Prompt and issue the following.

{lang="text",linenos=off}
	$ echo %PYTHONPATH%


If all works, you should then see output that looks something similar to the example below. On a Windows-based machine, you will obviously see a Windows path, most likely originating from the C drive.

{lang="text",linenos=off}
	/opt/local/Library/Frameworks/Python.framework/
	    Versions/2.7/lib/python2.7/site-packages:

This is the path to your Python installation's `site-packages` directory, where additional Python packages and modules are stored. If you see a path, you can continue to the next part of this tutorial. If you however do not see anything, you'll need to do a little bit of detective work to find out the path. On a Windows installation, this should be a trivial exercise: `site-packages` is located within the `lib` directory of your Python installation directory. For example, if you installed Python to `C:\Python27`, `site-packages` will be at `C:\Python27\Lib\site-packages\`.

UNIX-based operating systems however require a little bit of detective work to discover the path of your `site-packages` installation. To do this, launch the Python interpreter. The following terminal session demonstrates the commands you should issue.

{lang="text",linenos=off}
	$ python
	
	Python 2.7.5 (v2.7.5:ab05e7dd2788, May 13 2013, 13:18:45)
	[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	
	>>> import site
	>>> print(site.getsitepackages()[0])
	
	'/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages'
	
	>>> quit()

Calling `site.getsitepackages()` returns a list of paths that point to additional Python package and module stores. The first typically returns the path to your `site-packages` directory - changing the list index position may be required depending on your installation. If you receive an error stating that `getsitepackages()` is not present within the `site` module, verify you're running the correct version of Python. Version 2.7.5 should include this function. Previous versions of the language do not include this function.

The string which is shown as a result of executing `print site.getsitepackages()[0]` is the path to your installation's `site-packages` directory. Taking the path, we now need to add it to your configuration. On a UNIX-based or UNIX-derived operating system, edit your `.bashrc` file once more, adding the following to the bottom of the file.

{lang="text",linenos=off}
	export PYTHONPATH=$PYTHONPATH:<PATH_TO_SITE-PACKAGES>

Replace `<PATH_TO_SITE-PACKAGES>` with the path to your `site-packages` directory. Save the file, and quit and reopen any instances of your terminal.

On a Windows-based computer, you must follow the [instructions shown above](#section-system-setup-python-windows) to bring up the environment variables settings dialog. Add a `PYTHONPATH` variable with the value being set to your `site-packages` directory, which is typically `C:\Python27\Lib\site-packages\`.

## Using `setuptools` and `pip`
Installing and setting up your development environment is a really important part of any project. While it is possible to install Python Packages such as Django separately, this can lead to numerous problems and hassles later on. For example, how would you share your setup with another developer? How would you set up the same environment on your new machine? How would you upgrade to the latest version of the package? Using a package manager removes much of the hassle involved in setting up and configuring your environment. It will also ensure that the package you install is the correct for the version of Python you are using, along with installing any other packages that are dependent upon the one you want to install.

In this book, we use `pip`. `pip` is a user friendly wrapper over the `setuptools` Python package manager. Because `pip` depends on `setuptools`, we are required to ensure that both are installed on your computer.

To start, we should download `setuptools` from the [official Python package website](https://pypi.python.org/pypi/setuptools/1.1.6). You can download the package in a compressed `.tar.gz` file. Using your favourite file extracting program, extract the files. They should all appear in a directory called `setuptools-1.1.6` - where `1.1.6` represents the `setuptools` version number. From a terminal instance, you can then change into the directory and execute the script `ez_setup.py` as shown below.

{lang="text",linenos=off}
	$ cd setuptools-1.1.6
	$ sudo python ez_setup.py

In the example above, we also use `sudo` to allow the changes to become system wide. The second command should install `setuptools` for you. To verify that the installation was successful, you should be able to see output similar to that shown below.

{lang="text",linenos=off}
	Finished processing dependencies for setuptools==1.1.6

Of course, `1.1.6` is substituted with the version of `setuptools` you are installing. If this line can be seen, you can move onto installing `pip`. This is a trivial process, and can be completed with one simple command. From your terminal instance, enter the following.

{lang="text",linenos=off}
	$ sudo easy_install pip

This command should download and install `pip`, again with system wide access. You should see the following output, verifying `pip` has been successfully installed.

{lang="text",linenos=off}
	Finished processing dependencies for pip

Upon seeing this output, you should be able to launch `pip` from your terminal. To do so, just type `pip`. Instead of an unrecognised command error, you should be presented with a list of commands and switches that `pip` accepts. If you see this, you're ready to move on!

I> ### No Sudo on Windows!
I> On Windows computers, follow the same basic process. You won't need to enter the `sudo` command, however.

## Virtual Environments
We're almost all set to go! However, before we continue, it's worth pointing out that while this setup is fine to begin with, there are some drawbacks. What if you had another Python application that requires a different version to run? Or you wanted to switch to the new version of Django, but still wanted to maintain your Django 1.7 project?

The solution to this is to use [virtual environments](http://simononsoftware.com/virtualenv-tutorial/). Virtual environments allow multiple installations of Python and their relevant packages to exist in harmony. This is the generally accepted approach to configuring a Python setup nowadays. They are pretty easy to setup, once you have `pip` installed, and you know the right commands. You need to install a couple of additional packages.

{lang="text",linenos=off}
    $ pip install virtualenv
    $ pip install virtualenvwrapper

The first package provides you with the infrastructure to create a virtual environment. See [a non-magical introduction to `pip` and Virtualenv for Python Beginners](http://dabapps.com/blog/introduction-to-pip-and-virtualenv-python/) by Jamie Matthews for details about using virtualenv. However, using just *virtualenv* alone is rather complex. The second package provides a wrapper to the functionality in the virtualenv package and makes life a lot easier.

If you are using a Linux/UNIX based OS, then to use the wrapper you need to call the following shell script from your command line: :

{lang="text",linenos=off}
	$ source virtualenvwrapper.sh

It is a good idea to add this to your bash/profile script. So you don't have to run it each and every time you want to use virtual environments. However, if you are using windows, then install the [virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win) package:

{lang="text",linenos=off}
	$ pip install virtualenvwrapper-win

Now you should be all set to create a virtual environment:

{lang="text",linenos=off}
	$ mkvirtualenv rango

You can list the virtual environments created with `lsvirtualenv`, and you can activate a virtual environment as follows:

{lang="text",linenos=off}
	$ workon rango
	(rango)$

Your prompt with change and the current virtual environment will be displayed, i.e. `rango`. Now within this environment you will be able to install all the packages you like, without interfering with your standard or other environments. Try `pip list` to see you don't have Django or Pillow installed in your virtual environment. You can now install them with `pip` so that they exist in your virtual environment.

## Version Control
We should also point out that when you develop code, you should always house your code within a version controlled repository such as [SVN](http://subversion.tigris.org/) or [Git](http://git-scm.com/). We have provided a [chapter on using Git](#chapter-git) if you haven't used Git and GitHub before. We highly recommend that you set up a Git repository for your own projects. Doing so could save you from disaster.

X> ###Exercises
X> To get comfortable with your environment, try out the following exercises.
X>
X> - Install Python 2.7.5+ or Python 3.4+ and `pip`.
X> - Play around with your CLI and create a directory called `code`, which we use to create our projects in.
X> - Install the Django and Pillow packages.
X> - Setup your Virtual Environment
X> - Setup your account on GitHub
X> - Download and setup a Integrated Development Environment like [PyCharm Edu](https://www.jetbrains.com/pycharm-edu/download/).
X> - We have made the code for the book and application that you build available on GitHub, see [Tango With Django Book](https://github.com/leifos/tango_with_django_book) and [Rango Application](https://github.com/leifos/tango_with_django).
X> - If you spot any errors or problem with the book, you can make a change request!
X> - If you have any problems with the exercises, you can check out the repository and see how we completed them.
