import os
import os
import sys
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

# Append the parent directory to the sys.path to ensure create_env is accessible
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from create_env import setup_environment

# Set up environment variables
setup_environment()

from data_manager import DataManager
from preprocessor import Preprocessor
from feature_extractor import FeatureExtractor
from model_trainer import ModelTrainer


def process_nifti(preprocessor: Preprocessor, input_file: str):
	"""
	Process a single NIfTI file using the given preprocessor.

	This function takes a NIfTI file path and processes it using the specified
	preprocessor. If an error occurs during processing, it logs the error message
	without interrupting the execution flow.

	:param: preprocessor: An instance of Preprocessor used to handle the image processing.
	:param: input_file: str, the path to the NIfTI file to be processed.
	"""
	try:
		preprocessor.process_image(input_file)
	except Exception as e:
		print(f"Error processing {input_file}: {e}")


def process_images_sequentially(preprocessor, nifti_files):
	for input_file in tqdm(nifti_files, desc='Processing images', unit='file'):
		try:
			preprocessor.process_image(input_file)
		except Exception as e:
			print(f"Error processing {input_file}: {e}")
			continue


def process_images_in_parallel(preprocessor, nifti_files):
	with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
		futures = {executor.submit(process_nifti, preprocessor, input_file): input_file for input_file in nifti_files}
		with tqdm(total=len(nifti_files), desc="Processing images", unit='file') as pbar:
			for future in as_completed(futures):
				try:
					future.result()
				except Exception as e:
					input_file = futures[future]
					print(f"Error processing {input_file} with parallel execution: {e}")
				finally:
					pbar.update(1)


def main():
	"""
	Main function to manage the full MRI pre-processing and classification pipeline.
	"""

	# Initialize data manager for handling data operations
	data_manager = DataManager()
	
	# # Extract and organize DICOM files from ZIP archives
	# data_manager.process_zip_folders()

	# # Convert DICOM series to NIfTI
	# data_manager.convert_all_dicom_to_nifti()

	# Retrieve list of NIfTI files
	nifti_files = data_manager.get_nifti_files()
	
	# Initialize preprocessor and extract features
	preprocessor = Preprocessor()
	feature_extractor = FeatureExtractor()

	# Sequential processing of NIfTI files
	# process_images_sequentially(preprocessor, nifti_files)

	# Parallel processing of NIfTI files
	process_images_in_parallel(preprocessor, nifti_files)

	# Obtain labels and encode them
	labels_one_hot, df_labels = data_manager.encode_labels()

	# Prepare training data
	X_images, X_features = feature_extractor.prepare_training_data(segmented_image_files, df_labels)

	# Initialize model trainer and build model
	model_trainer = ModelTrainer()
	model = model_trainer.build_combined_model(X_images.shape[1:], X_features.shape[1:], num_classes=labels_one_hot.shape[1])

	# Train model
	model_trainer.train_model(model, X_images, X_features, labels_one_hot)

if __name__ == "__main__":
	main()
