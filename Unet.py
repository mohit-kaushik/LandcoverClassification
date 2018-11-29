from tensorflow.python.keras import losses
from tensorflow.python.keras import models
from tensorflow.python.keras import metrics
from tensorflow.python.keras import optimizers

def conv_block(input_x, n_filters):
	# 3 *3 kernel size, no. of kernels = n_filters, padding=keep input size same
	img_encoded = layers.Conv2D(n_filters, (3, 3), padding='same')(input_x)
	img_encoded = layers.BatchNormalization()(img_encoded)
	img_encoded = layers.Activation('relu')(img_encoded)
	img_encoded = layers.Conv2D(num_filters, (3, 3), padding='same')(img_encoded)
	img_encoded = layers.BatchNormalization()(img_encoded)
	img_encoded = layers.Activation('relu')(img_encoded)
	return img_encoded

def encoder_block(input_x, n_filters):
	encoded = conv_block(input_x, n_filters)
	encoded_pool = layers.MaxPooling2D((2, 2), strides=(2, 2))(encoded)
	return encoded_pool, encoded
