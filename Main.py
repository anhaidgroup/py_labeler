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



def suggest_tags_comments_column_name(df):
    comments_col = ""
    tags_col = ""
    if "comments" not in df.columns:
        comments_col = "comments"
    if "tags" not in df.columns:
        tags_col = "tags"
    return [tags_col, comments_col]


def client_script():
    qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
    if not qwebchannel_js.open(QIODevice.ReadOnly):
        raise SystemExit(
            'Failed to load qwebchannel.js with error: %s' %
            qwebchannel_js.errorString())
    qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')
    script = QWebEngineScript()
    script.setSourceCode(qwebchannel_js)
    script.setName('qWebChannelJS')
    script.setWorldId(QWebEngineScript.MainWorld)
    script.setInjectionPoint(QWebEngineScript.DocumentReady)
    script.setRunsOnSubFrames(True)
    return script


class MainPage(QWebEnginePage):
    def __init__(self):
        super(MainPage, self).__init__(None)

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

    @pyqtSlot(str, str)
    def respond(self, comments_col, tags_col):
        # todo 4/26/17 use local version - global df may refer to other data frame
        initialize_tags_comments(ApplicationContext.COMPLETE_DATA_FRAME, comments_col, tags_col)
        html_str = Renderer.render_main_page(
            current_page_tuple_pairs=ApplicationContext.PAGINATION_CONTROLLER.get_tuples_for_page(ApplicationContext.current_page_number),
            match_count=ApplicationContext.STATS_CONTROLLER.count_matched_tuple_pairs(ApplicationContext.current_data_frame),
            not_match_count=ApplicationContext.STATS_CONTROLLER.count_non_matched_tuple_pairs(ApplicationContext.current_data_frame),
            not_sure_count=ApplicationContext.STATS_CONTROLLER.count_not_sure_tuple_pairs(ApplicationContext.current_data_frame),
            unlabeled_count=ApplicationContext.STATS_CONTROLLER.count_not_labeled_tuple_pairs(ApplicationContext.current_data_frame)
        )
        self.setHtml(html_str)


def launch_labeler(file_name, attributes, label_column_name):
    df = read_data_frame(file_name,
                         attributes, label_column_name)

    ApplicationContext.COMPLETE_DATA_FRAME = df
    ApplicationContext.current_data_frame = df

    [tags_col, comments_col] = suggest_tags_comments_column_name(ApplicationContext.COMPLETE_DATA_FRAME)

    application = QApplication([])
    view = QWebEngineView()
    main_page = MainPage()
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
    pagination_controller = PaginationController(main_page)
    label_controller = LabelUpdateController(main_page)

    ApplicationContext.FILTER_CONTROLLER = filter_controller
    ApplicationContext.STATS_CONTROLLER = stats_controller
    ApplicationContext.PAGINATION_CONTROLLER = pagination_controller
    ApplicationContext.LABEL_CONTROLLER = label_controller

    channel.registerObject('bridge', main_page)
    channel.registerObject('filter_controller', filter_controller)
    channel.registerObject('stats_controller', stats_controller)
    channel.registerObject('pagination_controller', pagination_controller)
    channel.registerObject('label_controller', label_controller)
    view.show()

    application.exec_()


# execution starts here
launch_labeler('./test/data/drug_sample.csv',
               ["id", "ProductNo", "Form", "Dosage", "drugname", "activeingred", "ReferenceDrug", "ProductMktStatus"], "label")
