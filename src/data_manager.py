# The `DataManager` class provides methods to extract, organize, convert, and encode medical imaging
# data stored in DICOM format to NIfTI format, along with handling directory structures and generating
# labels based on the data.
import os
import zipfile
import shutil
import dicom2nifti
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


class DataManager:
	def __init__(self):
		"""
		Initialize DataManager with specified raw and processed paths.
		"""
		# Paths
		self.downloaded_data_path = os.getenv('DOWNLOADED_DATA_PATH')
		self.root_data_path = os.getenv('ROOT_DATA_PATH')
		self.raw_data_path = os.path.join(self.root_data_path, 'raw_data\\')
		self.raw_dicom_path = os.path.join(self.raw_data_path, 'dicom\\')
		self.raw_nifti_path = os.path.join(self.raw_data_path, 'nifti\\')
		self.processed_data_path = os.path.join(self.root_data_path, 'processed_data\\')


	def extract_and_organize_dicom(self, zip_directory):
		"""
		Extract DICOM files from zipped folders, restructure, and rename them.

		:param zip_directory: Path to the ZIP file containing DICOM files.
		"""
		try:
			# Extract filename and derive patient information
			base_name = os.path.basename(zip_directory)[:-4]
			parts = os.path.basename(zip_directory)[:-4].split('_')
			
			# Expecting format like "M_AD_50_74.zip"
			if len(parts) != 4:
				print(f"Unexpected filename format: {base_name}")
				return

			genre, stage, min_age, max_age = parts
			age = '_'.join([min_age, max_age])
			

			# Create base output directory using the extracted base name
			specific_output_dir = os.path.join(self.raw_dicom_path, genre, stage, age)
			os.makedirs(specific_output_dir, exist_ok=True)
			
			# Unzip contents
			with zipfile.ZipFile(zip_directory, 'r') as zip_ref:
				# Assuming the ZIP file is structured with a single root folder containing "ADNI"
				extracted_root_dir = os.path.join(self.raw_dicom_path, base_name + '_extracted')
				zip_ref.extractall(extracted_root_dir)

			# Counter for renaming folders consecutively
			series_counter = 1

			# Navigate the extracted directories to locate DICOM series
			for dirpath, dirnames, filenames in os.walk(extracted_root_dir):
				if any(fname.endswith('.dcm') for fname in filenames):
					new_folder_name = f"series_{series_counter}"
					dest_folder = os.path.join(specific_output_dir, new_folder_name)

					# Copy the folder containing DICOM files to the specific output directory with the new name
					shutil.copytree(dirpath, dest_folder, dirs_exist_ok=True)
					series_counter += 1

			# Clean up the extracted folder after processing
			shutil.rmtree(extracted_root_dir)

			print(f"Extraction and organization completed for {zip_directory}")

		except zipfile.BadZipFile:
			print(f"The ZIP file {zip_directory} is corrupted and cannot be opened.")

		except Exception as e:
			print(f"Error processing ZIP file {zip_directory}: {e}")


	def process_zip_folders(self):
		"""
		Process all ZIP files in a folder to extract and organize DICOM files.
		"""
		for zip_filename in os.listdir(self.downloaded_data_path):
			zip_file = os.path.join(self.downloaded_data_path, zip_filename)
			if zipfile.is_zipfile(zip_file):
				# Extract and organize each ZIP archive
				self.extract_and_organize_dicom(zip_file)


	def dicom_to_nifti(self, series_folder):
		"""
		Convert a folder of DICOM files to a NIfTI file using dicom2nifti.		
		:param series_folder: Path to the folder containing DICOM files.
		"""
		try:
			# Check the number of DICOM files in the directory and ensure there are enough slices
			if len([f for f in os.listdir(series_folder) if f.endswith('.dcm')]) < 3:
				print(f"Skipped: {series_folder}. Reason: TOO_FEW_SLICES/LOCALIZER")
				return

			# Calculate the base relative path without the "series_x", by getting the grandparent directory relative to series_folder
			rel_path = os.path.relpath(os.path.dirname(series_folder), self.raw_dicom_path)

			# Set the output folder path maintaining the original hierarchy
			output_folder = os.path.join(self.raw_nifti_path, rel_path)
			os.makedirs(output_folder, exist_ok=True)

			# Use the series folder name for the NIfTI file
			final_nifti_file_path = os.path.join(output_folder, os.path.basename(series_folder) + '.nii')

			# List files before conversion
			files_before = set(os.listdir(output_folder))

			# Convert DICOM to NIfTI
			dicom2nifti.convert_directory(series_folder, output_folder, compression=False, reorient=True)

			# Identify the newly created file
			new_file = list(set(os.listdir(output_folder)) - files_before)

			# Rename the file
			if new_file:
				os.rename(os.path.join(output_folder, new_file[0]), os.path.join(output_folder, final_nifti_file_path))

		except Exception as e:
			print(f"Error converting {series_folder} to NIfTI: {e}")


	def convert_all_dicom_to_nifti(self):
		"""
		Convert all organized DICOM series in the raw path to NIfTI files.

		This method iterates over all directories in the raw path, converts
		series of DICOM files to NIfTI format, and saves them in the processed path.
		"""
		# Navigate the extracted directories to locate DICOM series
		for dirpath, dirnames, filenames in os.walk(self.raw_dicom_path):
			if any(fname.endswith('.dcm') for fname in filenames):
				self.dicom_to_nifti(dirpath)

			print(f"Completed processing for all DICOM series in: {dirpath}")


	def get_nifti_files(self):
		"""
		Retrieve all NIfTI files from the processed path.

		This method walks through the processed path and collects paths
		for all .nii files present in the directory structure.

		:return: List of full paths to NIfTI files.
		"""
		nifti_files = []
		for root, _, files in os.walk(self.raw_nifti_path):
			for file in files:
				if file.endswith('.nii'):
					nifti_files.append(os.path.join(root, file))
		return nifti_files


	def get_labels_from_structure(self):
		"""
		Generate labels based on directory structure genre/stage/minage_maxage.

		:return: DataFrame with filenames and corresponding labels.
		"""
		data = []
		
		for genre in os.listdir(self.raw_path):
			genre_path = os.path.join(self.raw_path, genre)
			if not os.path.isdir(genre_path):
				continue
			
			for stage in os.listdir(genre_path):
				stage_path = os.path.join(genre_path, stage)
				if not os.path.isdir(stage_path):
					continue
				
				for age_range in os.listdir(stage_path):
					age_path = os.path.join(stage_path, age_range)
					if not os.path.isdir(age_path):
						continue
					
					for filename in os.listdir(age_path):
						if filename.endswith('.nii'):
							# Maintain an entry for each file
							data.append({
								'file_path': os.path.join(age_path, filename),
								'genre': genre,
								'stage': stage,
								'age_range': age_range.replace('_', '-')
							})

		return pd.DataFrame(data)


	def encode_labels(self, label_column='stage'):
		"""
		Encode the specified label column using OneHotEncoder.

		:param label_column: Column in DataFrame to be used for encoding.
		:return: numpy array of encoded labels.
		"""
		# Obtain label categories from environment
		

		# Get labels from structure
		df_labels = self.get_labels_from_structure()

		# Encode the specified label_column
		encoder = OneHotEncoder(sparse=False, categories=[df_labels])
		labels_one_hot = encoder.fit_transform(df_labels[[label_column]])
		
		return labels_one_hot, df_labels
