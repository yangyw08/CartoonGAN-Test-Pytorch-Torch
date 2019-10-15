import torch
import os
import numpy as np
import time
import argparse
from torch import cuda
from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.utils as vutils
from network.Transformer import Transformer

model_path = ""
style = ""
valid_ext = ['.jpg', '.png']

class CartoonGan():
    def __init__(self, model_path='./pretrained_model', style='Hayao', valid_ext=['.jpg', '.png'], input_dir='test_img', output_dir='test_output'):
        self.load_size = 450
        self.model_path = model_path
        self.style = style
        self.valid_ext = valid_ext
        # load pretrained model
        self.model = Transformer()
        self.model.load_state_dict(torch.load(os.path.join(self.model_path, self.style + '_net_G_float.pth')))
        self.model.eval()
        # GPU CPU
        if cuda.is_available():
            # if opt.gpu > -1:
            print('GPU mode')
            self.model.cuda()
        else:
            print('CPU mode')
            self.model.float()
    #
    def cartoon(self, download_file_path, processed_file_path):
        #
        ext = os.path.splitext(download_file_path)[1]
        if ext not in valid_ext:
            print("wrong format:", ext)
            return
        # load image
        input_image = Image.open(download_file_path).convert("RGB")
        # resize image, keep aspect ratio
        h = input_image.size[0]
        w = input_image.size[1]
        ratio = h * 1.0 / w
        if ratio > 1:
            h = self.load_size
            w = int(h * 1.0 / ratio)
        else:
            w = self.load_size
            h = int(w * ratio)
        input_image = input_image.resize((h, w), Image.BICUBIC)
        input_image = np.asarray(input_image)
        # RGB -> BGR
        input_image = input_image[:, :, [2, 1, 0]]
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)
        # preprocess, (-1, 1)
        input_image = -1 + 2 * input_image
        if cuda.is_available():
            # if opt.gpu > -1:
            input_image = Variable(input_image, volatile=True).cuda()
        else:
            input_image = Variable(input_image, volatile=True).float()
        # forward
        output_image = self.model(input_image)
        output_image = output_image[0]
        # BGR -> RGB
        output_image = output_image[[2, 1, 0], :, :]
        # deprocess, (0, 1)
        output_image = output_image.data.cpu().float() * 0.5 + 0.5
        # save
        vutils.save_image(output_image, processed_file_path)

if __name__ == '__main__':
    print("############################")
    origin_file = './test_img/lv.jpg'
    processed_file = './test_output/lv.jpg'
    begin_time = time.time()
    CartoonGan().cartoon(origin_file,processed_file)
    end_time = time.time()
    cost_time = end_time - begin_time
    print("cost time = ", cost_time)
    print("!!!!!!!!!!!!!!over!!!!!!!!!!!!!!")
    print("############################")
