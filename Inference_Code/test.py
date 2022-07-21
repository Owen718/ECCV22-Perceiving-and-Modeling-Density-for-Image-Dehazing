import os
import torch
import numpy as np
from torchvision import transforms
from PIL import Image
import time
import torchvision
import cv2
import torchvision.utils as tvu
import torch.functional as F
import argparse

def inference_img(haze_path,Net):
    
    haze_image = Image.open(haze_path).convert('RGB')
    enhance_transforms = transforms.Compose([
    transforms.Resize((400,400)),
    transforms.ToTensor()
    ])

    print(haze_image.size)
    with torch.no_grad():
        haze_image = enhance_transforms(haze_image)
        haze_image = haze_image.cuda().unsqueeze(0)
        start = time.time()
        restored2 = Net(haze_image)
        end = time.time()


    return restored2,end-start

if __name__ == '__main__': 
    parser=argparse.ArgumentParser()    
    parser.add_argument('--test_path',type=str,required=True,help='Path to test')
    parser.add_argument('--save_path',type=str,required=True,help='Path to save')
    parser.add_argument('--pk_path',type=str,required=True,help='Path of the checkpoint')
    opt = parser.parse_args()
    test_list = os.listdir(opt.test_path)
    Net=torch.jit.load(opt.pk_path,map_location=torch.device('cuda:0')).eval().cuda()
    for i,image in enumerate(test_list):
        print(image)
        restored2,time_num = inference_img(os.path.join(opt.test_path,image),Net)
        torchvision.utils.save_image(restored2,os.path.join(opt.save_path,image))
