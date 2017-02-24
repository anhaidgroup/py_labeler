from PyQt5.Qt import *
from OpenGL import GL  # Do not auto clean imports !! from OpenGL import GL is needed for linux

# todo 2/23/17  issue seems to be with linux
# todo 2/23/17  check error with blank screen. ref: https://riverbankcomputing.com/pipermail/pyqt/2014-January/033681.html

qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
if not qwebchannel_js.open(QIODevice.ReadOnly):
    raise SystemExit(
        'Failed to load qwebchannel.js with error: %s' %
        qwebchannel_js.errorString())
qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')


def client_script():
    script = QWebEngineScript()
    script.setSourceCode(qwebchannel_js + '''
    new QWebChannel(qt.webChannelTransport, function(channel) {
        channel.objects.bridge.respond('Hello world!');
    });

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
    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

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
