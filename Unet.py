from tensorflow.python.keras import losses
from tensorflow.python.keras import models
from tensorflow.python.keras import metrics
from tensorflow.python.keras import optimizers

def conv_block(input_x, n_filters):
	# 3 *3 kernel size, no. of kernels = n_filters, padding=keep input size same
	img_encoded = layers.Conv2D(n_filters, (3, 3), padding='same')(input_x)
	img_encoded = layers.BatchNormalization()(img_encoded)
	img_encoded = layers.Activation('relu')(img_encoded)
	img_encoded = layers.Conv2D(n_filters, (3, 3), padding='same')(img_encoded)
	img_encoded = layers.BatchNormalization()(img_encoded)
	img_encoded = layers.Activation('relu')(img_encoded)
	return img_encoded

def encoder_block(input_x, n_filters):
	encoded = conv_block(input_x, n_filters)
	encoded_pool = layers.MaxPooling2D((2, 2), strides=(2, 2))(encoded)
	return encoded_pool, encoded

def decoder_block(input_x, concat_x, n_filters):
	decoded_x = layers.Conv2DTranspose(n_filters, (2, 2), strides=(2, 2), padding='same')(input_x)
	decoded_x = layers.concatenate([concat_x, decoded_x], axis=-1) # axis(NHWC) -1=C, concatenate channel wise
	decoded_x = layers.BatchNormalization()(decoded_x)
	decoded_x = layers.Activation('relu')(decoded_x)

	decoded_x = layers.Conv2D(n_filters, (3, 3), padding='same')(decoded_x)
	decoded_x = layers.BatchNormalization()(decoded_x)
	decoded_x = layers.Activation('relu')(decoded_x)

	decoded_x = layers.Conv2D(n_filters, (3, 3), padding='same')(decoded_x)
	decoded_x = layers.BatchNormalization()(decoded_x)
	decoded_x = layers.Activation('relu')(decoded_x)
	
	return decoded_x

def get_model():
	# encoder0=256 padding same is used
	# Size None for a FCN
	inputs = layers.Input(shape=[None, None, 3]) # 256(encoder0_pool), /2 using maxpool
	encoder0_pool, encoder0 = encoder_block(inputs, 32) # 128(encoder1_pool), /2 using maxpool
	encoder1_pool, encoder1 = encoder_block(encoder0_pool, 64) # 64, /2 using maxpool
	encoder2_pool, encoder2 = encoder_block(encoder1_pool, 128) # 32, /2 using maxpool
	encoder3_pool, encoder3 = encoder_block(encoder2_pool, 256) # 16, /2 using maxpool
	encoder4_pool, encoder4 = encoder_block(encoder3_pool, 512) # 8, /2 using maxpool
	
	center = conv_block(encoder4_pool, 1024) # center
	
	decoder4 = decoder_block(center, encoder4, 512) # 16
	decoder3 = decoder_block(decoder4, encoder3, 256) # 32
	decoder2 = decoder_block(decoder3, encoder2, 128) # 64
	decoder1 = decoder_block(decoder2, encoder1, 64) # 128
	decoder0 = decoder_block(decoder1, encoder0, 32) # 256
	
	
	outputs = layers.Conv2D(1, (1, 1), activation='softmax')(decoder0)

	model = models.Model(inputs=[inputs], outputs=[outputs])

	model.compile(optimizer=optimizers.get('SGD'), loss=losses.get('CategoricalCrossentropy'),metrics=['categorical_accuracy'])

	return model
