import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from cartoonGan import *
import handler

define('port',default='9101',help='Listening port',type=int)

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/',handler.Index),
            (r'/upload', handler.Upload)
        ]
        settings = dict(
            debug = True,
            static_path = 'static'
        )
        #self.cartooner = CartoonGan()
        super(Application, self).__init__(handlers,**settings)

app = Application()

if __name__ == '__main__':
    #################################################################
    tornado.options.parse_command_line()
    app.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
