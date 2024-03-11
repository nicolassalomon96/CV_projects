import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imageio.v2 as io
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
import cv2
import torch
import os
import sys
device= "cuda" if torch.cuda.is_available() else "cpu"
#from img2vec_pytorch import Img2Vec # !pip install img2vec-pytorch - https://github.com/christiansafka/img2vec/blob/master/img2vec_pytorch/img_to_vec.py for more details
from tokenize_image import Tokenize_img

dataset_path = r'E:\Datasets\rock_paper_scissors'
classes = {0: 'rock', 1: 'paper', 2: 'scissors'}

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
emb_df = []
targets = []
for sign in classes.keys():
    filenames = os.listdir(os.path.join(dataset_path, f'{classes[sign]}'))
    for i, file in enumerate(filenames):
        with Image.open(fp=os.path.join(dataset_path, f'{classes[sign]}', file), mode='r') as img:
            #print(img)
            vector = embedder(img)
            vector = np.hstack([vector, sign])
            #emb_df.append(pd.Series(data=[vector, sign], index=['vector', 'sign']))
            emb_df.append(vector)
            #targets.append(sign)

#emb_df: [samples:2717, n_features:512 + 1(class)]

p_train = 0.8
emb_df = pd.DataFrame(emb_df)

train_df, test_df = train_test_split(emb_df, test_size = 0.20)

train_df = train_df.iloc[:,:-1]
test_df = test_df.iloc[:,:-1]

train_targets = train_df.iloc[:,-1].astype(int)
test_targets = test_df.iloc[:,-1].astype(int)

#USE SVM to create a Classifier
model = svm.SVC(kernel='poly', degree=2)
#print(train_df.shape, train_targets.shape)
model.fit(train_df, train_targets)

y_pred = model.predict(test_df)
print("Accuracy:", metrics.accuracy_score(test_targets, y_pred))