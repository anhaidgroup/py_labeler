# coding=utf-8
import logging
import os

from py_labeler.utils import install_path

logger = logging.getLogger(__name__)


def get_install_path():
    path_list = install_path.split(os.sep)
    return os.sep.join(path_list[0:len(path_list) - 1])
