import pandas as pd 
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np

vgg16_model = VGG16(weights='imagenet', include_top=False)

class DataCreation:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
    
    def load_data(self):
        # Load data from CSV
        self.data = pd.read_csv(self.data_path)
        # Example: Assuming 'image_link' column exists
        self.image_links = self.data['image_link'].tolist()
    
    def preprocess_images(self, image_links, image_size=(224, 224)):
        processed_images = []
        for image_link in image_links:
            try:
                # Load and preprocess image
                image = load_img(image_link, target_size=image_size)
                image_arr = img_to_array(image)
                image_arr = preprocess_input(image_arr)
                processed_images.append(image_arr)
            except Exception as e:
                print(f"Error processing image {image_link}: {e}")
                # Append a zero feature for error case
                processed_images.append(np.zeros((image_size[0], image_size[1], 3)))
        
        return np.array(processed_images)

    def process_batch(self, image_batch, image_links):
        # Convert list of images to a tensor
        image_batch_tensor = tf.convert_to_tensor(image_batch, dtype=tf.float32)
    
        # Expand dimensions if necessary (for model input)
        if len(image_batch_tensor.shape) == 3:
            image_batch_tensor = tf.expand_dims(image_batch_tensor, axis=0)
    
        # Extract features using VGG16
        features = vgg16_model.predict(image_batch_tensor)
    
        # Return features and corresponding image links
        return features.tolist(), image_links
    
    def create_features(self, batch_size=32):
        self.load_data()
        all_features = []
        all_links = []
        
        image_links = self.image_links
        for i in range(0, len(image_links), batch_size):
            batch_links = image_links[i:i+batch_size]
            image_batch = self.preprocess_images(batch_links)
            features, links = self.process_batch(image_batch, batch_links)
            all_features.extend(features)
            all_links.extend(links)
        
        return all_features, all_links
