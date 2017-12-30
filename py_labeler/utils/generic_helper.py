# coding=utf-8
import logging
import os

import pandas as pd
import six

# import py_labeler.catalog.catalog_manager as cm
from py_labeler.utils import install_path

# from py_labeler.utils.catalog_helper import check_fk_constraint

logger = logging.getLogger(__name__)


def get_install_path():
    path_list = install_path.split(os.sep)
    return os.sep.join(path_list[0:len(path_list) - 1])

