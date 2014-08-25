import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="autoreload during debug is true", type=bool)

class IndexHander(tornado.web.RequestHandler):
    def get(self):
        self.write("hello")

class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.i = 0
        self.callback = tornado.ioloop.PeriodicCallback(self._send_message, 800)
        self.callback.start()
        print ">> WebSocket opened"

    def on_message(self, message):
        print ">> Recieved message: " + message

    def on_close(self):
        self.callback.stop()
        print ">> WebSocket closed"

    def check_origin(self, origin):
        return True

    def _send_message(self):
        self.i += 1
        self.write_message(str(self.i))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers = [
        (r"/", IndexHander),
        (r"/socket", SocketHandler)
        ], debug = options.debug)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
