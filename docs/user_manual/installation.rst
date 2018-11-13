============
Installation
============

Requirements
------------
* Minimum Python 3.5+, Recommended Python 3.5.2+

Platforms
---------
py_labeler has been tested on Linux (Ubuntu 15, 16, 17), OS X (Sierra), and Windows 10.

Please ensure that your OS is 64-bit.

Dependencies
------------
* pandas (provides data structures to store and manage tables)
* pyqt5 (provides tools to build GUIs)
* jinja2 (provides templating for GUI)
* numpy (required by pandas)


Installing Using pip
--------------------
To install the package using pip, execute the following
command::

    pip install -U py_labeler


The above command will install py_labeler and all of its dependencies.

Note about working with conda/virtual environments
------------------------------------------
Due to dependencies, py_labeler works only with virtual environments created with virtualenv or a pure python 3.5+ environment.

We recommend working with a virtual environment created using the

    virtualenv

command.

If you are working with an environment created using conda note that conda does not provide the latest version of PyQt5 which py_labeler needs.
An already installed package such as jupyter which uses conda's version of PyQt5 may cause conflict with the version py_labeler needs.


Installing from Source Distribution
-----------------------------------
Clone the py_labeler package from GitHub

    git clone https://github.com/anhaidgroup/py_labeler.git

Then,  execute the following commands from the package root::

    python setup.py install

which installs py_labeler into the default Python directory on your machine. If you do not have installation permission for that directory then you can install the package in your
home directory as follows::

        python setup.py install --user

For more information see this StackOverflow `link <http://stackoverflow.com/questions/14179941/how-to-install-python-packages-without-root-privileges>`_.

The above commands will install py_labeler and all of its
dependencies.

Troubleshooting
-----------------------------------

- **ModuleNotFoundError: No module named PyQt5.sip**

Because the sip is installed separately, there may be some issues during the installation. Try to uninstall both pyqt5 and pyqt5-tools and then reinstall them.

- **ModuleNotFoundError: No module named 'PyQt5.QtWebEngineWidgets'**

PyQt5 for 32-bit OS does not contain the WebEngine modules. Please make sure both your OS and Python are 64-bit.

- **The program works but the display is strange**

Please check your network connection. Some templates requires external script files from the Internet.
