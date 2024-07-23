from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Load the model
model = load_model('VGG16_pneumonia_epoch_5.h5')

# Load and preprocess the image
image_path = 'hello.jpeg'
img = Image.open(image_path)
img = img.resize((224, 224))  # Example resize to match input size of the model
img_array = np.asarray(img)
img_array = img_array.astype('float32') / 255.0  # Normalize pixel values

# Add a dimension for batch (if required by the model)
img_array = np.expand_dims(img_array, axis=0)

# Make predictions
predictions = model.predict(img_array)

# Example of using the model's predictions
print(predictions)
