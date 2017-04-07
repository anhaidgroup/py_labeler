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
df = pd.read_csv('./test/sample.csv')

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

    @pyqtSlot(str)
    def respond(self, text):

        html_str = Renderer.render_horizontal_template(pagination_contoller.get_page(0),
                                                       ["ID", "birth_year", "name"], 0,
                                                       Constants.COUNT_PER_PAGE, ceil(df.shape[0] / Constants.COUNT_PER_PAGE),
                                                       total_count=stats_controller.count_tuple_pairs(df),
                                                       match_count=stats_controller.count_matched_tuple_pairs(df),
                                                       not_match_count=stats_controller.count_non_matched_tuple_pairs(df),
                                                       not_sure_count=stats_controller.count_not_sure_tuple_pairs(df),
                                                       unlabeled_count=stats_controller.count_not_labeled_tuple_pairs(df),
                                                       tokens_per_attribute=20
                                                       )

        # html_str = Renderer.render_main_page(pagination_contoller.get_page(1),
        #                                      pagination_contoller.get_current_page(),
        #                                      pagination_contoller.get_per_page_count(),
        #                                      pagination_contoller.get_number_of_pages(df),
        #                                      stats_controller.count_matched_tuple_pairs(df),
        #                                      stats_controller.count_non_matched_tuple_pairs(df),
        #                                      stats_controller.count_not_sure_tuple_pairs(df),
        #                                      stats_controller.count_tuple_pairs(df)
        #                                      )
        print(html_str)
        self.setHtml(html_str)
        # print(Renderer.render_main_page(df))
        # Renderer.renderSampleTemplate(title="templated page", users=["me", "them", "who"], data=df.to_dict()))
        # print('From JS:', Renderer.renderSampleTemplate(title="templated page", users=["me", "them", "who"]))


# execution starts here

# render_horizontal_template(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,match_count,                          not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute=50):



ht = Renderer.render_horizontal_template(df, ["ID", "birth_year", "name"], 2, None, 5, 100, 10, 11, 12, 13,
                                         tokens_per_attribute=20)
application = QApplication([])
main_page = MainPage()
main_page.profile().clearHttpCache()
main_page.profile().scripts().insert(client_script())  # insert QT web channel JS to allow for communication
view = QWebEngineView()
main_page.setHtml('<button id="hello">Start Labeling</button>')
view.setPage(main_page)

# create channel of communication between HTML & Py
channel = QWebChannel(main_page)
main_page.setWebChannel(channel)

# add controllers to the channel
filter_controller = FilterController(main_page, data_frame=df)
stats_controller = StatsController(main_page)
pagination_contoller = PaginationController(main_page)
label_controller = LabelUpdateController(main_page, df)
pagination_contoller.set_data(data_frame=df)
pagination_contoller.set_per_page_count(5)  # todo 4/7/17 change this to use Constants.py
pagination_contoller.set_current_page(0)

channel.registerObject('bridge', main_page)
channel.registerObject('filter_controller', filter_controller)
channel.registerObject('stats_controller', stats_controller)
channel.registerObject('pagination_controller', pagination_contoller)
channel.registerObject('label_controller', label_controller)
view.show()

application.exec_()
