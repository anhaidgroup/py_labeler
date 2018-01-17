py_labeler
=================

This project seeks to build a Python based GUI for manual labeling of
candidate pairs.

Given two tables A and B, the goal of
EM is to discover the tuple pairs between two tables that refer to the
same real-world entities. There are two main steps involved in entity matching:
blocking and matching. The blocking step aims to remove obvious non-matching
tuple pairs and reduce the set considered for matching. Entity matching in
practice involves many steps than just blocking and matching. While performing EM
users often execute many steps, e.g. exploring, cleaning, debugging, sampling,
estimating accuracy, etc. Current EM systems however do not cover the entire
EM pipeline, providing support only for a few steps (e.g., blocking, matching), while
ignoring less well-known yet equally critical steps (e.g., debugging, sampling).
py_entitymatching seeks to support all the steps involved in EM pipeline.

At the matching step, users would want to check and verify candidate pairs as matches
or non-matches. This is a manual process and this package py_labeler, provides a GUI to make this
process easier.

The package is free, open-source, and BSD-licensed.

Important links
===============

* Project Homepage: https://sites.google.com/site/anhaidgroup/projects/magellan/py_labeler_v0_1_1
* Code repository: https://github.com/anhaidgroup/py_labeler
* Issue Tracker: https://github.com/anhaidgroup/py_labeler/issues

Dependencies
============

The required dependencies to build the packages are:

* pandas (provides data structures to store and manage tables)
* pyqt5 (provides tools to build GUIs)
* jinja2 (provides templating for GUI)


Platforms
=========

py_labeler has been tested on Linux, OS X and Windows.
