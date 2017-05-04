from math import ceil

import pandas as pd
from OpenGL import GL
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineScript
from PyQt5.QtWidgets import QApplication

from controller.FilterController import FilterController
from controller.LabelUpdateController import LabelUpdateController
from controller.PaginationController import PaginationController
from controller.StatsController import StatsController
from utils import ApplicationContext
from view import Renderer


# do not auto clean imports! from OpenGL import GL is needed on linux
# ref: https://riverbankcomputing.com/pipermail/pyqt/2014-January/033681.html

# Global data frame so that it is common to the controllers

def read_data_frame(file_name, attribute_list, label_column):
    df = pd.read_csv(file_name)

    ApplicationContext.current_attributes = attribute_list
    ApplicationContext.ALL_ATTRIBUTES = ApplicationContext.current_attributes

    if label_column not in df.columns:
        # Add label column
        df[label_column] = "Not-Labeled"
    ApplicationContext.LABEL_COLUMN = label_column
    return df


def initialize_tags_comments(df, comments_col, tags_col):
    if comments_col not in df.columns:
        # initialize empty col
        df[comments_col] = ""
    if tags_col not in df.columns:
        # initialize empty col
        df[tags_col] = ""

    ApplicationContext.COMMENTS_COLUMN = comments_col
    ApplicationContext.TAGS_COLUMN = tags_col

    ApplicationContext.COMPLETE_DATA_FRAME = df
    ApplicationContext.current_data_frame = df
    return df


# todo 3/10/17 move this under view?
qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
if not qwebchannel_js.open(QIODevice.ReadOnly):
    raise SystemExit(
        'Failed to load qwebchannel.js with error: %s' %
        qwebchannel_js.errorString())
qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')

df = read_data_frame('./test/data/drug_sample.csv',
                     ["id", "ProductNo", "Form", "Dosage", "drugname", "activeingred", "ReferenceDrug", "ProductMktStatus"], "label")


def suggest_tags_comments_column_name(df):
    comments_col = ""
    tags_col = ""
    if "comments" not in df.columns:
        comments_col = "comments"
    if "tags" not in df.columns:
        tags_col = "tags"
    return [tags_col, comments_col]


[tags_col, comments_col] = suggest_tags_comments_column_name(df)


def client_script():
    script = QWebEngineScript()
    script.setSourceCode(qwebchannel_js)
    script.setName('qWebChannelJS')
    script.setWorldId(QWebEngineScript.MainWorld)
    script.setInjectionPoint(QWebEngineScript.DocumentReady)
    script.setRunsOnSubFrames(True)
    return script


class MainPage(QWebEnginePage):
    def __init__(self, df):
        super(MainPage, self).__init__(None)
        self.df = df

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

    @pyqtSlot(str, str)
    def respond(self, comments_col, tags_col):
        # todo 4/26/17 use local version - global df may refer to other data frame
        global df
        df = initialize_tags_comments(df, comments_col, tags_col)
        html_str = Renderer.render_main_page(current_page_tuple_pairs=pagination_contoller.get_page(0),
                                             match_count=stats_controller.count_matched_tuple_pairs(df),
                                             not_match_count=stats_controller.count_non_matched_tuple_pairs(df),
                                             not_sure_count=stats_controller.count_not_sure_tuple_pairs(df),
                                             unlabeled_count=stats_controller.count_not_labeled_tuple_pairs(df)
                                             )
        print(html_str)
        self.setHtml(html_str)


# execution starts here

application = QApplication([])
view = QWebEngineView()
main_page = MainPage(df)
main_page.profile().clearHttpCache()
main_page.profile().scripts().insert(client_script())  # insert QT web channel JS to allow for communication
main_page.setHtml(Renderer.render_options_page(tags_col, comments_col))
view.setPage(main_page)

# create channel of communication between HTML & Py
channel = QWebChannel(main_page)
main_page.setWebChannel(channel)

# add controllers to the channel
filter_controller = FilterController(main_page)
stats_controller = StatsController(main_page)
pagination_contoller = PaginationController(main_page)
label_controller = LabelUpdateController(main_page)

channel.registerObject('bridge', main_page)
channel.registerObject('filter_controller', filter_controller)
channel.registerObject('stats_controller', stats_controller)
channel.registerObject('pagination_controller', pagination_contoller)
channel.registerObject('label_controller', label_controller)
view.show()

application.exec_()
