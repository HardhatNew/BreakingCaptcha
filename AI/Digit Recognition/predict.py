from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
import numpy

# Load the trained model
model = load_model('digit_recognition_model.h5')

# Load and prepare the input image
image = load_img('example_image.png', grayscale=True, target_size=(28, 28))
image = img_to_array(image)
image = image.reshape(-1, 28, 28, 1)
image = image / 255.0

# Predict the image using the model
prediction = model.predict(image)
predicted_label = numpy.argmax(prediction)
print('Predicted Digit:', predicted_label)