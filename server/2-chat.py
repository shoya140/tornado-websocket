import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="autoreload during debug is true", type=bool)

class Board(object):
    lastMessage = ""
    callbacks = []

    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)

    def notifyCallbacks(self):
        for callback in self.callbacks:
            callback(self.lastMessage)

    def updateMessage(self, message):
        self.lastMessage = message
        self.notifyCallbacks()

class IndexHander(tornado.web.RequestHandler):
    def get(self):
        self.write("hello")

class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.board.register(self.callback)

    def on_message(self, message):
        self.application.board.updateMessage(message)

    def on_close(self):
        self.application.board.unregister(self.callback)

    def check_origin(self, origin):
        return True

    def callback(self, message):
        self.write_message(message)

class Application(tornado.web.Application):
    def __init__(self):
        self.board = Board()
        handlers = [
            (r"/", IndexHander),
            (r"/socket", SocketHandler)
        ]
        settings = {"debug":options.debug}
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
