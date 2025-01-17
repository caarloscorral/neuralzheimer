from tensorflow.keras.models import Model
from tensorflow.keras import layers, Input


class ModelTrainer:
	def __init__(self):
		"""
		Initialize ModelTrainer to create, train, and evaluate deep learning models.
		"""
		pass


	def build_combined_model(self, input_shape_images, input_shape_features):
		"""
		Constructs a neural network model that combines 3D image data with derived features.

		:param input_shape_images: Shape of the volumetric image input.
		:param input_shape_features: Shape of the derived feature input.
		:return: Compiled Keras model ready for training.
		"""
		# Image input branch (3D CNN)
		image_input = Input(shape=input_shape_images)
		x = layers.Conv3D(32, kernel_size=(3, 3, 3), activation='relu')(image_input)
		x = layers.MaxPooling3D(pool_size=(2, 2, 2))(x)
		x = layers.Flatten()(x)
		
		# Feature input branch
		feature_input = Input(shape=input_shape_features)
		y = layers.Dense(32, activation='relu')(feature_input)
		
		# Combine both branches
		combined = layers.concatenate([x, y])
		z = layers.Dense(64, activation='relu')(combined)
		output = layers.Dense(1, activation='sigmoid')(z)
		
		# Create and compile model
		model = Model(inputs=[image_input, feature_input], outputs=output)
		model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
		return model


	def train_model(self, model, X_images, X_features, labels):
		"""
		Train the model using volumetric images and derived features.

		:param model: The Keras model to be trained.
		:param X_images: Numpy array of image data.
		:param X_features: Numpy array of feature data.
		:param labels: Array of ground truth labels.
		"""
		model.fit(
			[X_images, X_features],
			labels,
			epochs=50,
			batch_size=8,
			validation_split=0.2
		)
