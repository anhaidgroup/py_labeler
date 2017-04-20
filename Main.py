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
from utils import Constants
from view import Renderer


# do not auto clean imports! from OpenGL import GL is needed on linux
# ref: https://riverbankcomputing.com/pipermail/pyqt/2014-January/033681.html

# todo 3/26/17 move to constants file?
# Global data frame so that it is common to the controllers
def initialize_data(comments_col, tags_col):
    df = pd.read_csv('./test/drug_sample.csv')
    # df = df.drop_duplicates(subset='_id', keep='last')
    # df = df.set_index(['_id'], verify_integrity=True, drop=False)

    Constants.COMMENTS_COLUMN = comments_col
    Constants.TAGS_COLUMN = tags_col

    # todo 4/14/17 check if these columns exist already
    df[Constants.COMMENTS_COLUMN] = ""
    df[Constants.TAGS_COLUMN] = ""
    df[Constants.LABEL_COLUMN] = "Not-Labeled"

    Constants.complete_data = df
    Constants.current_data = df

    Constants.attributes = ["id", "ProductNo", "Form", "Dosage", "drugname", "activeingred", "ReferenceDrug", "ProductMktStatus"]
    Constants.ALL_ATTRIBUTES = Constants.attributes
    return df


# todo 3/10/17 move this under view?
qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
if not qwebchannel_js.open(QIODevice.ReadOnly):
    raise SystemExit(
        'Failed to load qwebchannel.js with error: %s' %
        qwebchannel_js.errorString())
qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')


def client_script():
    script = QWebEngineScript()
    script.setSourceCode(qwebchannel_js + '''
    var button = document.getElementById('hello');
    button.onclick = function(){
    new QWebChannel(qt.webChannelTransport, function(channel) {
     channel.objects.bridge.respond('button clicked!!');
    });}
    ''')
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
        df = initialize_data(comments_col, tags_col)

        html_str = Renderer.render_main_page(tuple_pairs=pagination_contoller.get_page(0),
                                             attributes=Constants.attributes, current_page=0,
                                             count_per_page=Constants.COUNT_PER_PAGE, number_of_pages=ceil(df.shape[0] / Constants.COUNT_PER_PAGE),
                                             total_count=stats_controller.count_tuple_pairs(df),
                                             match_count=stats_controller.count_matched_tuple_pairs(df),
                                             not_match_count=stats_controller.count_non_matched_tuple_pairs(df),
                                             not_sure_count=stats_controller.count_not_sure_tuple_pairs(df),
                                             unlabeled_count=stats_controller.count_not_labeled_tuple_pairs(df),
                                             tokens_per_attribute=Constants.TOKENS_PER_ATTRIBUTE
                                             )
        print(html_str)
        self.setHtml(html_str)
        # print(Renderer.render_main_page(df))
        # Renderer.renderSampleTemplate(title="templated page", users=["me", "them", "who"], data=df.to_dict()))
        # print('From JS:', Renderer.renderSampleTemplate(title="templated page", users=["me", "them", "who"]))


# execution starts here
application = QApplication([])
main_page = MainPage()
main_page.profile().clearHttpCache()
main_page.profile().scripts().insert(client_script())  # insert QT web channel JS to allow for communication
view = QWebEngineView()
main_page.setHtml(Renderer.render_options_page())
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
