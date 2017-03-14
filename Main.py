import pandas as pd
from OpenGL import GL
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineScript
from PyQt5.QtWidgets import QApplication

from controller.FilterController import FilterController
from controller.PaginationController import PaginationController
from controller.StatsController import StatsController
from view import Renderer

# do not auto clean imports! from OpenGL import GL is needed on linux
# ref: https://riverbankcomputing.com/pipermail/pyqt/2014-January/033681.html

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
        df = pd.read_csv('./test/sample.csv')

        self.setHtml(
            Renderer.render_main_page(df)
        )
        print(Renderer.render_main_page(df))
        # Renderer.renderSampleTemplate(title="templated page", users=["me", "them", "who"], data=df.to_dict()))
        # print('From JS:', Renderer.renderSampleTemplate(title="templated page", users=["me", "them", "who"]))


# execution starts here
application = QApplication([])
main_page = MainPage()
main_page.profile().scripts().insert(client_script())  # insert QT web channel JS to allow for communication
view = QWebEngineView()
main_page.setHtml('<button id="hello">Start Labeling</button>')
view.setPage(main_page)

# create channel of communication between HTML & Py
channel = QWebChannel(main_page)
main_page.setWebChannel(channel)

# add controllers to the channel
filter_controller = FilterController()
stats_controller = StatsController()
pagination_contoller = PaginationController()
channel.registerObject('bridge', main_page)
channel.registerObject('filter_controller', filter_controller)
channel.registerObject('stats_controller', stats_controller)
channel.registerObject('pagination_controller', pagination_contoller)
view.show()

application.exec_()
