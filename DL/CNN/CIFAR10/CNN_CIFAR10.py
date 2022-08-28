# -*- coding: utf-8 -*-
"""CNN_CIFAR10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SjZmi6t8jSPDdQzwr5msY1xHh_wSdQ13

## Connect to drive
"""

from google.colab import drive
drive.mount('/gdrive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /gdrive/My Drive/AI/CNN/CIFAR10

"""## Imports"""

import tensorflow as tf
import numpy as np
import os
import random
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix

tfk = tf.keras
tfkl = tf.keras.layers

# Download and import visualkeras library
!pip install visualkeras
import visualkeras



"""## Set seed"""

seed = 42
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)
np.random.seed(seed)

"""## Load data

CIFAR10 dataset
"""

# Import dataset and plit it
(X_train_val , y_train_val) , (X_test, y_test) = tfk.datasets.cifar10.load_data()
labels = {0:'airplane', 1:'automobile', 2:'bird', 3:'cat', 4:'deer', 5:'dog', 6:'frog', 7:'horse', 8:'ship', 9:'truck'}
X_train_val.shape

"""## Inspect the data"""

num_row = 2
num_col = 5
fig, axes = plt.subplots(num_row, num_col, figsize=(10*num_row,2*num_col))
for i in range(num_row*num_col):
    ax = axes[i//num_col, i%num_col]
    ax.imshow(X_train_val[i])
    ax.set_title('{}'.format(labels[y_train_val[i][0]]))
plt.tight_layout()
plt.show()

"""## Preprocessing data"""

# Normalization

X_train_val = X_train_val / 255.
X_test = X_test / 255.

# Labels to categorical (one hot)
y_train_val = tfk.utils.to_categorical(y_train_val)
y_test = tfk.utils.to_categorical(y_test)

# Split validation and train
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, random_state=seed, test_size = 0.1, stratify=y_train_val)

"""## Models metadata"""

input_shape = X_train.shape[1:]
batch_size = 128
epochs = 200

"""## Build the Model"""

def build_model(input_shape):
  input_layer = tfkl.Input(shape=input_shape, name="InputLayer")
  # CNN part
  conv1 = tfkl.Conv2D(
      filters=8,
      kernel_size=(3, 3),
      strides = (1, 1),
      padding = 'same',
      activation = 'relu',
      kernel_initializer = tfk.initializers.GlorotUniform(seed)
  )(input_layer)
  conv2 = tfkl.Conv2D(
      filters=16,
      kernel_size=(3, 3),
      strides = (1, 1),
      padding = 'same',
      activation = 'relu',
      kernel_initializer = tfk.initializers.GlorotUniform(seed)
  )(conv1)
  pool1 = tfkl.MaxPooling2D(
      pool_size = (2, 2)
  )(conv2)

  conv3 = tfkl.Conv2D(
      filters=32,
      kernel_size=(3, 3),
      strides = (1, 1),
      padding = 'same',
      activation = 'relu',
      kernel_initializer = tfk.initializers.GlorotUniform(seed)
  )(pool1)
  conv4 = tfkl.Conv2D(
      filters=64,
      kernel_size=(3, 3),
      strides = (1, 1),
      padding = 'same',
      activation = 'relu',
      kernel_initializer = tfk.initializers.GlorotUniform(seed)
  )(conv3)
  pool2 = tfkl.MaxPooling2D(
      pool_size = (2, 2)
  )(conv4)

  conv5 = tfkl.Conv2D(
      filters=128,
      kernel_size=(3, 3),
      strides = (1, 1),
      padding = 'same',
      activation = 'relu',
      kernel_initializer = tfk.initializers.GlorotUniform(seed)
  )(pool2)
  pool3 = tfkl.MaxPooling2D(
      pool_size = (2, 2)
  )(conv5)

  # FC part
  flattening_layer = tfkl.Flatten()(pool3)
  flattening_layer = tfkl.Dropout(0.3,seed=seed)(flattening_layer)
  classifier_layer = tfkl.Dense(units = 256, activation='relu')(flattening_layer)
  classifier_layer = tfkl.Dropout(0.2,seed=seed)(classifier_layer)
  hidden_layer = tfkl.Dense(units = 256, activation='relu')(classifier_layer)
  hidden_layer = tfkl.Dropout(0.1,seed=seed)(hidden_layer)
  output_layer = tfkl.Dense(units=10, activation='softmax')(hidden_layer)

  model = tfk.Model(inputs=input_layer, outputs=output_layer, name='CIFAR_model')

  model.compile(loss=tfk.losses.CategoricalCrossentropy(), optimizer=tfk.optimizers.Adam(), metrics='accuracy')
  return model

model = build_model(input_shape)
print(model.summary())
visualkeras.layered_view(model, legend=True, spacing=20, scale_xy=10)

"""# Train the model"""

# Train the model
history = model.fit(
    x = X_train,
    y = y_train,
    batch_size = batch_size,
    epochs = epochs,
    validation_data = (X_val, y_val),
    callbacks = [tfk.callbacks.EarlyStopping(monitor='val_accuracy', mode='max', patience=10, restore_best_weights=True)]
).history

# Plot the training
plt.figure(figsize=(15,5))
plt.plot(history['loss'], label='Training', alpha=.8, color='#ff7f0e')
plt.plot(history['val_loss'], label='Validation', alpha=.8, color='#4D61E2')
plt.legend(loc='upper left')
plt.title('Binary Crossentropy')
plt.grid(alpha=.3)

plt.figure(figsize=(15,5))
plt.plot(history['accuracy'], label='Training', alpha=.8, color='#ff7f0e')
plt.plot(history['val_accuracy'], label='Validation', alpha=.8, color='#4D61E2')
plt.legend(loc='upper left')
plt.title('Accuracy')
plt.grid(alpha=.3)

plt.show()

"""# Testing"""

# Predict the test set with the CNN
predictions = model.predict(X_test)
predictions.shape

# Compute the confusion matrix
cm = confusion_matrix(np.argmax(y_test, axis=-1), np.argmax(predictions, axis=-1))

# Compute the classification metrics
accuracy = accuracy_score(np.argmax(y_test, axis=-1), np.argmax(predictions, axis=-1))
precision = precision_score(np.argmax(y_test, axis=-1), np.argmax(predictions, axis=-1), average='macro')
recall = recall_score(np.argmax(y_test, axis=-1), np.argmax(predictions, axis=-1), average='macro')
f1 = f1_score(np.argmax(y_test, axis=-1), np.argmax(predictions, axis=-1), average='macro')
print('Accuracy:',accuracy.round(4))
print('Precision:',precision.round(4))
print('Recall:',recall.round(4))
print('F1:',f1.round(4))

# Plot the confusion matrix
plt.figure(figsize=(10,8))
sns.heatmap(cm.T, xticklabels=list(labels.values()), yticklabels=list(labels.values()))
plt.xlabel('True labels')
plt.ylabel('Predicted labels')
plt.show()

"""## Test with my image"""

from PIL import Image
image = Image.open("dog.png")
image_crop = image.resize((32,32),Image.ANTIALIAS)
image_arr = np.array(image_crop, dtype=np.float32)[:,:,:3]
prediction = model.predict(image_arr[None, ...])
prediction[0]

# Plot the target images and the predictions

fig, (ax1, ax2) = plt.subplots(1,2)
fig.set_size_inches(15,5)
ax1.imshow(image)
ax2.barh(list(labels.values()), prediction[0], color=plt.get_cmap('Paired').colors)
ax2.set_title('Predicted label: '+labels[np.argmax(prediction[0])])
ax2.grid(alpha=.3)
plt.show()

plt.show()