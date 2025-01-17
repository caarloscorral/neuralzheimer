import ants
import numpy as np
import pandas as pd

class FeatureExtractor:
	def __init__(self):
		"""
		Initialize FeatureExtractor to handle extraction and computation of features
		from segmented MRI images.
		"""
		pass


	def calculate_tissue_volume(self, segmented_image):
		"""
		Calculate the volume of the segmented tissue in cubic millimeters.

		:param segmented_image: ANTsPy image of segmented tissue.
		:return: Volume of the tissue.
		"""
		return segmented_image.sum() * np.prod(segmented_image.spacing)


	def extract_features(self, gm_path, wm_path, csf_path):
		"""
		Extract features like tissue volumes given paths to segmented images.

		:param gm_path: NIfTI file path for grey matter segmentation.
		:param wm_path: NIfTI file path for white matter segmentation.
		:param csf_path: NIfTI file path for CSF segmentation.
		:return: A dictionary with extracted features.
		"""
		gm_img = ants.image_read(gm_path)
		wm_img = ants.image_read(wm_path)
		csf_img = ants.image_read(csf_path)

		features = {
			'gm_volume': self.calculate_tissue_volume(gm_img),
			'wm_volume': self.calculate_tissue_volume(wm_img),
			'csf_volume': self.calculate_tissue_volume(csf_img)
		}
		# Print extracted feature volumes for inspection
		print(f"Extracted Features: GM Volume: {features['gm_volume']}, WM Volume: {features['wm_volume']}, CSF Volume: {features['csf_volume']}")
		return features


	def prepare_training_data(self, segmented_image_files, feature_data):
		"""
		Combine volumetric images with derived features for training.

		:param segmented_image_files: List of file paths to segmented images.
		:param feature_data: DataFrame containing derived features such as tissue volumes.
		:return: Tuple of numpy arrays: (image arrays, feature arrays).
		"""
		X_images = []
		X_features = []

		for idx, img_file in enumerate(segmented_image_files):
			img = ants.image_read(img_file)
			X_images.append(img.numpy())

			feature_row = feature_data.iloc[idx].to_numpy()
			X_features.append(feature_row)

		return np.array(X_images), np.array(X_features)
