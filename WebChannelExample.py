from PyQt5.Qt import *

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
        channel.objects.bridge.print('Hello world!');
    });
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
    def print(self, text):
        print('From JS:', text)


app = QApplication([])
p = WebPage()
v = QWebEngineView()
v.setPage(p)
p.profile().scripts().insert(client_script())
c = QWebChannel(p)
p.setWebChannel(c)
c.registerObject('bridge', p)
v.setHtml('<p>Hello world!')
v.show()
app.exec_()
