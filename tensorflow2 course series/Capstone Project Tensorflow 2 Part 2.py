#!/usr/bin/env python
# coding: utf-8

# # Capstone Project
# ## Image classifier for the SVHN dataset
# ### Instructions
# 
# In this notebook, you will create a neural network that classifies real-world images digits. You will use concepts from throughout this course in building, training, testing, validating and saving your Tensorflow classifier model.
# 
# This project is peer-assessed. Within this notebook you will find instructions in each section for how to complete the project. Pay close attention to the instructions as the peer review will be carried out according to a grading rubric that checks key parts of the project instructions. Feel free to add extra cells into the notebook as required.
# 
# ### How to submit
# 
# When you have completed the Capstone project notebook, you will submit a pdf of the notebook for peer review. First ensure that the notebook has been fully executed from beginning to end, and all of the cell outputs are visible. This is important, as the grading rubric depends on the reviewer being able to view the outputs of your notebook. Save the notebook as a pdf (File -> Download as -> PDF via LaTeX). You should then submit this pdf for review.
# 
# ### Let's get started!
# 
# We'll start by running some imports, and loading the dataset. For this project you are free to make further imports throughout the notebook as you wish. 

# In[25]:


import tensorflow as tf
from scipy.io import loadmat

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, BatchNormalization, MaxPool2D, Dense
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import EarlyStopping

from tensorflow.keras.layers import Dropout
from tensorflow.keras import regularizers

import random


# ![SVHN overview image](data/svhn_examples.jpg)
# For the capstone project, you will use the [SVHN dataset](http://ufldl.stanford.edu/housenumbers/). This is an  image dataset of over 600,000 digit images in all, and is a harder dataset than MNIST as the numbers appear in the context of natural scene images. SVHN is obtained from house numbers in Google Street View images. 
# 
# * Y. Netzer, T. Wang, A. Coates, A. Bissacco, B. Wu and A. Y. Ng. "Reading Digits in Natural Images with Unsupervised Feature Learning". NIPS Workshop on Deep Learning and Unsupervised Feature Learning, 2011.
# 
# Your goal is to develop an end-to-end workflow for building, training, validating, evaluating and saving a neural network that classifies a real-world image into one of ten classes.

# In[26]:


# Run this cell to load the dataset

train = loadmat('data/train_32x32.mat')
test = loadmat('data/test_32x32.mat')


# Both `train` and `test` are dictionaries with keys `X` and `y` for the input images and labels respectively.

# ## 1. Inspect and preprocess the dataset
# * Extract the training and testing images and labels separately from the train and test dictionaries loaded for you.
# * Select a random sample of images and corresponding labels from the dataset (at least 10), and display them in a figure.
# * Convert the training and test images to grayscale by taking the average across all colour channels for each pixel. _Hint: retain the channel dimension, which will now have size 1._
# * Select a random sample of the grayscale images and corresponding labels from the dataset (at least 10), and display them in a figure.

# In[10]:


x_train = train['X']
y_train = train['y']
x_test = test['X']
y_test = test['y']

y_train = y_train - 1
y_test = y_test - 1


# In[11]:


x_train = np.moveaxis(x_train, -1, 0)
x_test = np.moveaxis(x_test, -1 , 0)


# In[23]:


for i in range(10):
    plt.imshow(x_train[i, :, :, :,])
    plt.show()
    print(y_train[i])


# In[13]:


x_train_grayscale = tf.image.rgb_to_grayscale(x_train)


# In[21]:


for i in range(10):
    plt.imshow(x_train_grayscale[i][:, :, 0], cmap='gray')
    plt.show()
    print(y_train[i])


# In[ ]:





# ## 2. MLP neural network classifier
# * Build an MLP classifier model using the Sequential API. Your model should use only Flatten and Dense layers, with the final layer having a 10-way softmax output. 
# * You should design and build the model yourself. Feel free to experiment with different MLP architectures. _Hint: to achieve a reasonable accuracy you won't need to use more than 4 or 5 layers._
# * Print out the model summary (using the summary() method)
# * Compile and train the model (we recommend a maximum of 30 epochs), making use of both training and validation sets during the training run. 
# * Your model should track at least one appropriate metric, and use at least two callbacks during training, one of which should be a ModelCheckpoint callback.
# * As a guide, you should aim to achieve a final categorical cross entropy training loss of less than 1.0 (the validation loss might be higher).
# * Plot the learning curves for loss vs epoch and accuracy vs epoch for both training and validation sets.
# * Compute and display the loss and accuracy of the trained model on the test set.

# In[3]:


model = Sequential([
    Flatten(input_shape=(32, 32, 3)),
    Dense(64, kernel_regularizer=regularizers.l2(1e-5), activation='relu'),
    Dropout(0.3),
    Dense(64, kernel_regularizer=regularizers.l2(1e-5), activation='relu'),
    BatchNormalization(),
    Dense(64, kernel_regularizer=regularizers.l2(1e-5), activation='relu'),
    Dropout(0.3),
    Dense(10, activation='softmax')
])


# In[4]:


model.summary()


# In[5]:


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['acc'])


# In[6]:


model_checkpoint = ModelCheckpoint(filepath = 'my_checkpoint_MLP', save_best_only=True, save_weights_only=True, monitor='val_loss')
earlystopping = EarlyStopping(patience=5, monitor='loss')


# In[12]:


history = model.fit(x=x_train, y=y_train, 
                    batch_size=128, 
                    validation_data=(x_test, y_test), 
                    epochs=5,
                    callbacks=[model_checkpoint, earlystopping])


# In[100]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')


# In[103]:


plt.plot(history.history['acc'], label='Training Accuracy')
plt.plot(history.history['val_acc'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')


# In[104]:


model.evaluate(x_test, y_test, verbose=2)


# ## 3. CNN neural network classifier
# * Build a CNN classifier model using the Sequential API. Your model should use the Conv2D, MaxPool2D, BatchNormalization, Flatten, Dense and Dropout layers. The final layer should again have a 10-way softmax output. 
# * You should design and build the model yourself. Feel free to experiment with different CNN architectures. _Hint: to achieve a reasonable accuracy you won't need to use more than 2 or 3 convolutional layers and 2 fully connected layers.)_
# * The CNN model should use fewer trainable parameters than your MLP model.
# * Compile and train the model (we recommend a maximum of 30 epochs), making use of both training and validation sets during the training run.
# * Your model should track at least one appropriate metric, and use at least two callbacks during training, one of which should be a ModelCheckpoint callback.
# * You should aim to beat the MLP model performance with fewer parameters!
# * Plot the learning curves for loss vs epoch and accuracy vs epoch for both training and validation sets.
# * Compute and display the loss and accuracy of the trained model on the test set.

# In[14]:


model2 = Sequential([
    
    Conv2D(16, kernel_size= 3, activation='relu', input_shape=(32, 32, 3)),
    MaxPool2D(pool_size= (3,3), strides=1),
    Conv2D(32, kernel_size = 3, padding='valid', strides=1, activation='relu'),
    MaxPool2D(pool_size = (1,1), strides = 3),
    BatchNormalization(),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(10, activation='softmax')
])


# In[7]:


model2.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['acc'])


# In[8]:


model2.summary()


# In[19]:


model_checkpoint = ModelCheckpoint(filepath = 'my_checkpoint', save_best_only=True, save_weights_only=True, monitor='val_loss')
earlystopping = EarlyStopping(patience=5, monitor='loss')


# In[ ]:


history = model2.fit(x=x_train, y=y_train, 
                    batch_size=64, 
                    validation_data=(x_test, y_test), 
                    epochs=5,
                    callbacks=[model_checkpoint, earlystopping])


# In[11]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')


# In[12]:


plt.plot(history.history['acc'], label='Training Accuracy')
plt.plot(history.history['val_acc'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')


# In[13]:


model2.evaluate(x_test, y_test, verbose=2)


# ## 4. Get model predictions
# * Load the best weights for the MLP and CNN models that you saved during the training run.
# * Randomly select 5 images and corresponding labels from the test set and display the images with their labels.
# * Alongside the image and label, show each model’s predictive distribution as a bar chart, and the final model prediction given by the label with maximum probability.

# In[15]:


model.load_weights('my_checkpoint_MLP')
model2.load_weights('my_checkpoint')


# In[22]:


num_samples_to_display = 5
random_indices = np.random.choice(len(x_test), num_samples_to_display, replace=False)
x_samples = x_test[random_indices]
y_samples = y_test[random_indices]


# In[23]:


def display_image_prediction(image, predictions, label, model_name):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title(f'Label: {label}')
    
    plt.subplot(1, 2, 2)
    plt.bar(range(10), predictions)
    plt.xticks(range(10))
    plt.xlabel('Class Index')
    plt.ylabel('Probability')
    plt.title(f'{model_name} Predictions')
    
    plt.show()


# In[24]:


for i in range(num_samples_to_display):
    sample_image = x_samples[i]
    label = y_samples[i]
    
    mlp_predictions = model.predict(np.expand_dims(sample_image, axis=0))
    cnn_predictions = model2.predict(np.expand_dims(sample_image, axis=0))
    
    display_image_prediction(sample_image, mlp_predictions[0], label, 'MLP')
    display_image_prediction(sample_image, cnn_predictions[0], label, 'CNN')


# In[ ]:





# In[ ]:




