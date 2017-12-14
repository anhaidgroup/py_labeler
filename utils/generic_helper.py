# coding=utf-8
import logging
import os

import pandas as pd
import six

import py_entitymatching.catalog.catalog_manager as cm
from utils import install_path
from py_entitymatching.utils.catalog_helper import check_fk_constraint

logger = logging.getLogger(__name__)


def get_install_path():
    path_list = install_path.split(os.sep)
    return os.sep.join(path_list[0:len(path_list) - 1])


def remove_non_ascii(s):
    if not isinstance(s, six.string_types):
        logger.error('Property name is not of type string')
        raise AssertionError('Property name is not of type string')
    s = ''.join(i for i in s if ord(i) < 128)
    s = str(s)
    return str.strip(s)


# find list difference
def list_diff(a_list, b_list):
    if not isinstance(a_list, list) and not isinstance(a_list, set):
        logger.error('a_list is not of type list or set')
        raise AssertionError('a_list is not of type list or set')

    if not isinstance(b_list, list) and not isinstance(b_list, set):
        logger.error('b_list is not of type list or set')
        raise AssertionError('b_list is not of type list or set')

    b_set = list_drop_duplicates(b_list)
    return [a for a in a_list if a not in b_set]


def load_dataset(file_name, key=None, **kwargs):
    if not isinstance(file_name, six.string_types):
        logger.error('file name is not a string')
        raise AssertionError('file name is not a string')
    p = get_install_path()
    p = os.sep.join([p, 'datasets', file_name + '.csv'])
    table = pd.read_csv(p, **kwargs)
    if key is not None:
        cm.set_key(table, key)
    return table


# remove rows with NaN in a particular attribute
def rem_nan(table, attr):
    if not isinstance(table, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')
    if not isinstance(attr, six.string_types):
        logger.error('Input attr. should be of type string')
        raise AssertionError('Input attr. should be of type string')

    if not attr in table.columns:
        logger.error('Input attr not in the table columns')
        raise KeyError('Input attr. not in the table columns')

    l = table.index.values[pd.np.where(table[attr].notnull())[0]]
    return table.ix[l]


def list_drop_duplicates(lst):
    if not isinstance(lst, list) and not isinstance(lst, set):
        logger.error('Input object not of type list or set')
        raise AssertionError('Input object is not of type list or set')

    a = []
    for i in lst:
        if i not in a:
            a.append(i)
    return a


# data frame with output attributes
def create_proj_dataframe(df, key, key_vals, attrs, col_names):
    if not isinstance(df, pd.DataFrame):
        logger.error('Input object is not of type pandas data frame')
        raise AssertionError('Input object is not of type pandas data frame')

    if not isinstance(key, six.string_types):
        logger.error('Input key is not of type string')
        raise AssertionError('Input key is not of type string')

    if not key in df.columns:
        logger.error('Input key is not in the dataframe columns')
        raise KeyError('Input key is not in the dataframe columns')

    df = df.set_index(key, drop=False)
    df = df.ix[key_vals, attrs]
    df.reset_index(drop=True, inplace=True)
    df.columns = col_names
    return df


def del_files_in_dir(dir):
    if os.path.isdir(dir):
        filelist = [f for f in os.listdir(dir)]
        for f in filelist:
            p = os.sep.join([dir, f])
            # print(p)
            os.remove(p)


def creat_dir_ifnot_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def convert_to_str_unicode(input_string):
    if not isinstance(input_string, six.string_types):
        input_string = six.u(str(input_string))

    if isinstance(input_string, bytes):
        input_string = input_string.decode('utf-8', 'ignore')

    return input_string
