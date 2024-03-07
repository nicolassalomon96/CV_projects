import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imageio.v2 as io
import pandas as pd
import cv2
import torch
import os
import sys
device= "cuda" if torch.cuda.is_available() else "cpu"
#from img2vec_pytorch import Img2Vec # !pip install img2vec-pytorch - https://github.com/christiansafka/img2vec/blob/master/img2vec_pytorch/img_to_vec.py for more details
from tokenize_image import Tokenize_img

dataset_path = r'E:\Datasets\rock_paper_scissors'
classes = ['rock', 'paper', 'scissors']

class Image_embeddings():
    def __init__(self, cuda=True, model='resnet-18', layer_output_size=512):
        self.use_cuda = cuda
        self.model = model
        self.layer_output_size = layer_output_size
        self.img2vec = Tokenize_img(cuda=self.use_cuda, model=self.model, layer_output_size=self.layer_output_size)

    def __call__(self, image):
        emb_vec = self.img2vec.get_vec(image) #Embedding Vector of the codified image
        return emb_vec

embedder = Image_embeddings()
emb_list = []
for sign in classes:
    filenames = os.listdir(os.path.join(dataset_path, sign))
    for i, file in enumerate(filenames):
        with Image.open(fp=os.path.join(dataset_path, sign, file), mode='r') as img:
            #print(img)
            vector = embedder(img)
            emb_list.append(pd.Series(data=[vector, sign], index=['vector', 'sign']))
        
emb_df = pd.DataFrame(emb_list)

#USE SVM to create a Classifier