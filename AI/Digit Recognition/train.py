from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import KFold
import numpy

# Load MNIST dataset (digit images)
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Reshape/preprocess the data
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)
x_train = x_train / 255.0
x_test = x_test / 255.0
y_train = to_categorical(y_train, num_classes=10)
y_test = to_categorical(y_test, num_classes=10)

# Create image data generators for data augmentation
train_datagen = ImageDataGenerator(
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator()

# Build the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Evaludate the model using k-fold cross-validation
def model_evaluation(dataX, dataY, k, epoch):
    print('[Model Evaluation]')
    kfold = KFold(k, shuffle=True, random_state=1)
    fold = 0  # fold count
    accuracies = []  # store all accuracy
    losses = []  # store all losses
    for train_ix, test_ix in kfold.split(dataX):
        fold += 1
        print('K:', fold)
        X_train, Y_train, X_test, Y_test = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
        # Fit the image data generators on the data
        train_datagen.fit(X_train)
        test_datagen.fit(X_test)
        train_iterator = train_datagen.flow(X_train, Y_train, batch_size=32)
        test_iterator = test_datagen.flow(X_test, Y_test, batch_size=32)
        # Fit the model
        model.fit(train_iterator, epochs=epoch, validation_data=test_iterator)
        # Evaluate the model
        loss, accuracy = model.evaluate(X_test, Y_test)
        losses.append(loss)
        accuracies.append(accuracy)
    return numpy.mean(loss), numpy.mean(accuracies)

# Call the model evaluation
loss, accuracy = model_evaluation(x_train, y_train, 3, 5)
print('Average loss:', loss)
print('Average accuracy:', accuracy,'\n')

# Fit the image data generators on the data
train_datagen.fit(x_train)
test_datagen.fit(x_test)
train_iterator = train_datagen.flow(x_train, y_train, batch_size=32)
test_iterator = test_datagen.flow(x_test, y_test, batch_size=32)

# Fit model for the actual training
print('[Model Training]')
model.fit(train_iterator, epochs=5, validation_data=test_iterator)
    
# Save the model
model.save('digit_recognition_model.h5')
