# Handwritten Digit Recognition
This is a simple digit recognition model using TensorFlow. This model uses CNN which consists of several layers that apply filters to the input image. It also uses Categorical Cross-entropy loss and Adam optimizer which are common for image recognition tasks. The MNIST (digits) dataset is chosen for its popularity (widely used) and easy accessibility. The dataset contains 60000 training samples and 10000 test samples.

## Preparation
These are the packages used in the code:

 - from tensorflow.keras.datasets import mnist
 - from tensorflow.keras.utils import to_categorical
 - from tensorflow.keras.models import Sequential
 - from tensorflow.keras.layers import Conv2D
 - from tensorflow.keras.layers import MaxPooling2D
 - from tensorflow.keras.layers import Flatten
 - from tensorflow.keras.layers import Dense
 - from tensorflow.keras.preprocessing.image import ImageDataGenerator
 - from tensorflow.keras.models import load_model
 - from tensorflow.keras.preprocessing.image import load_img
 - from tensorflow.keras.preprocessing.image import img_to_array
 - from sklearn.model_selection import KFold
 - import numpy

So, make sure the necessary requisites like **TensorFlow, NumPy, scikit-learn** are installed in order to run the code successfully.

## Running the code
The model has been trained, hence we can skip the initial training and run ‘predict.py’ directly.
There are 2 python files and 1 example image:

- train.py: trains the model and saves it to 'digit_recognition_model.h5'
- predict.py: loads the trained model 'digit_recognition_model.h5' to predict the given input image
- example_image.png: an example image of the digit 6 to run the prediction

> **Note:** The path to the input image will need to be adjusted manually for each image when running the prediction.

## Understanding the code
First, it loads and splits the MNIST dataset into train and test sets where the x contain the images and y contain their corresponding labels. The next following lines prepare the data by reshaping it (the values are based on the dataset: 28x28 pixels, greyscale) and normalizing it (division by 255.0). The 'to_categorical' function converts the labels into binary forms (length 10, since 0-9 digits). The ‘ImageDataGenerator’ is used for data augmentation to create different variants of the dataset by rotating (up to 20 degrees), zooming (up to 15 degrees), shifting, etc. This will then be applied to train dataset while leave test dataset as is.

Next is building the CNN model. The first layer (Conv2D) applies 32 filters with size of 3x3 to extract the features of the input image. The second layer (MaxPooling2D) is a pooling window with size of 2x2 to downsample the feature maps while the Flatten layer is a layer that flattens the feature maps. The fourth and the fifth layer (Dense) each with different value and activation. Then, the code compiles the model with Categorical Cross-entropy loss which is popular for multi-class classifications, and Adam optimizer which is common for recognition tasks.

Next is a function called 'model_evaluation' which takes dataX, dataY, k (number of folds), and epoch (epoch value) as the parameter to do k-fold cross-validation. Its function is to evaluate a model's ability/skill on new data. It works by splitting the dataset into k number of folds, each fold passes the entire training data by the epoch value. Inside the function, we have several variables, to keep count of fold and to store accuracies and losses for later average (mean) calculation. When shuffling is true, the random_state 1 allows it to maintain the intial and last value whie randomizing the rest. We can also see assignment of selected samples by index to the new X_train, Y_train, etc. Then, the datagen is fitted to the new Xs and uses the 'flow' method to create iterators to generate augmented batches, which will then be used for inputs to fit the model. The 'evaluate' function will evaluate the model, returning the loss and accuracy.

After getting satisfied with the result, we finally fit the whole training and test dataset from MNIST for the actual training of the model. The last line saves the model into a .h5 file ('digit_recognition_model.h5') to be used for predictions. The prediction code inputs an image, prepares it similar to the model code, then it makes the prediction using the trained model.

## Example input and output
Here, we run 'predict.py' which takes example_image.png as the input for the prediction.

![example_image.png](https://i.imgur.com/TaLGBOK.png)

![running predict.py on example_image.png](https://i.imgur.com/Bgmc6uU.png)

## Things to improve
We can hyper tune the parameters to achieve a better accuracy, also experimenting with different algorithms and optimizers such as SGD which generally performs better but takes longer time. Furthermore, we can add more datasets or variants to each data classes and apply more strategies to improve the accuracy.

## Suggestions for development
Deploying it to the website, providing an interface for the user to draw and perform real time prediction. Similarly, this model could be modified to predict alphabet letters.

## References
 - Jason Brownlee, ‘How to Develop a CNN for MNIST Handwritten Digit Classification’, Machine Learning Mastery, May 2019. Accessed on: May 4, 2023. [Online]. Available: https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-from-scratch-for-mnist-handwritten-digit-classification/
 - Wei-Meng Lee, ‘Image Data Augmentation for Deep Learning’, Towards Data Science, Oct. 2022. Accessed on: May 12, 2022. [Online]. Available: https://towardsdatascience.com/image-data-augmentation-for-deep-learning-77a87fabd2bf
 - Kang & Atul, ‘ImageDataGenerator – flow method’, TheAILearner, Jul. 2019. Accessed on: May 14, 2022. [Online]. Available: https://theailearner.com/2019/07/06/imagedatagenerator-flow-method/
 - Jason Brownlee, ‘A Gentle Introduction to k-fold Cross-Validation’, Machine Learning Mastery, May 2018. Accessed on: May 17, 2022. [Online]. Available: https://machinelearningmastery.com/k-fold-cross-validation/
 - Siladittya Manna, ‘K-Fold Cross Validation for Deep Learning Models using Keras’, Medium, Mar. 2020. Accessed on: May 19, 2022. [Online]. Available: https://medium.com/the-owl/k-fold-cross-validation-in-keras-3ec4a3a00538
 - LeCun, Y., Cortes, C. and Burges, C.J.C. (1998) The MNIST Database of Handwritten Digits. New York, USA. http://yann.lecun.com/exdb/mnist/