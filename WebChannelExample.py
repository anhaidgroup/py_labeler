from PyQt5.Qt import *
from PyQt5 import QtCore
from OpenGL import GL  # Do not auto clean imports !! from OpenGL import GL is needed for linux

# todo 2/23/17  issue seems to be with linux
# todo 2/23/17  check error with blank screen. ref: https://riverbankcomputing.com/pipermail/pyqt/2014-January/033681.html

qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
# todo 2/23/17 check http://lists.qt-project.org/pipermail/qtwebengine/2016-March/000339.html about injecting js to every file
if not qwebchannel_js.open(QIODevice.ReadOnly):
    raise SystemExit(
        'Failed to load qwebchannel.js with error: %s' %
        qwebchannel_js.errorString())
qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')


def client_script():
    script = QWebEngineScript()
    script.setSourceCode(qwebchannel_js + '''
//    new QWebChannel(qt.webChannelTransport, function(channel) {
//        channel.objects.bridge.respond('Hello world!');
//    });

    var button = document.getElementById('hello');
    button.onclick = function(){
     new QWebChannel(qt.webChannelTransport, function(channel) {
        channel.objects.bridge.respond('button clicked!!');
    });}
''')
    script.setName('xxx')
    script.setWorldId(QWebEngineScript.MainWorld)
    script.setInjectionPoint(QWebEngineScript.DocumentReady)
    script.setRunsOnSubFrames(True)
    return script


class WebPage(QWebEnginePage):
    # selectedText = pyqtProperty(str, notify=sigDataChanged)

    def __init__(self):
        super(WebPage, self).__init__(None)

    #     self.selectionChanged.connect(self.handleSelectionChange)
    #     self.titleChanged.connect(self.handleSelectionChange)

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

            # @pyqtSlot(str)
            # def handleSelectionChange(self):
            #     return
            # selectedText = pyqtProperty(str, notify=sigDataChanged)

    @pyqtSlot(str)
    def respond(self, text):
        print('From JS:', text)


app = QApplication([])
p = WebPage()
v = QWebEngineView()
v.setPage(p)
p.profile().scripts().insert(client_script())
c = QWebChannel(p)
p.setWebChannel(c)
c.registerObject('bridge', p)
p.setHtml('<button id="hello">Hello world!</button>')
p.setBackgroundColor(Qt.transparent)
v.show()

app.exec_()
