import tornado.web
import os
import json

class Index(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        #print("hello, world")
        self.write("hello,world\n")

class Upload(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.write(json.dumps({'url':'/static/cartoon/test.jpg'}))

    def post(self, *args, **kwargs):
        server_path_prefix = 'https://test.s.ads.sohu.com/'
        file_imgs = self.request.files.get('img',None)
        hex_color = self.get_argument("color", 'A25356')
        hex_color = hex_color.strip()
        hex_color = hex_color.lstrip('#')
        print("show color",hex_color)
        #print(hex_color)
        file_img =  file_imgs[0]
        image_key = hex_color + '_' + file_img['filename']
        image_download_path = 'static/uploads/{}'.format(image_key)
        image_processed_path = 'static/makeup/{}'.format(image_key)
        #print(type((file_img['body'])))
        with open(image_download_path, 'wb') as f:
                f.write(file_img['body'])
        rgb_color = self.HEX_to_RGB(hex_color)

        #print(file_imgs)
        self.write(json.dumps({'url':server_path_prefix + image_processed_path}))

    def HEX_to_RGB(self, hex):
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)
        return [r, g, b]


def HEX_to_RGB(hex):
    hex = hex.strip()
    hex = hex.lstrip('#')
    r = int(hex[0:2],16)
    g = int(hex[2:4],16)
    b = int(hex[4:6],16)
    return [r, g, b]

if __name__ == '__main__':
    #################################################################
    print(HEX_to_RGB("#A25356"))
