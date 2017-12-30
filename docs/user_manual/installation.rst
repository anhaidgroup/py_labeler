============
Installation
============

Requirements
------------
* Python 3.5+

Platforms
---------
py_labeler has been tested on Linux (Ubuntu 15, 16, 17), OS X (Sierra), and Windows 10.

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
