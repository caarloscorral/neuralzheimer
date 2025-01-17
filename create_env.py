import os
import configparser
from utils import find_software_path, add_paths_to_bashrc

def setup_environment():
	# Initialize ConfigParser
	config = configparser.ConfigParser()

	# Load the config.ini file
	config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
	
	# Check if the configuration file exists
	if not os.path.exists(config_path):
		raise FileNotFoundError(f"Configuration file not found at path: {config_path}")
	
	# Read configuration file and check for successful load
	config.read(config_path)

	# Add error checking for missing sections
	if 'PATHS' not in config:
		raise KeyError("Missing 'PATHS' section in configuration.")
	if 'DATA' not in config:
		raise KeyError("Missing 'DATA' section in configuration.")

	# Paths settings
	os.environ['DOWNLOADED_DATA_PATH'] = config['PATHS'].get('DOWNLOADED_DATA_PATH').strip().strip('"')
	os.environ['ROOT_DATA_PATH'] = config['PATHS'].get('ROOT_DATA_PATH').strip().strip('"')

	# Data settings
	os.environ['GENRES'] = config['DATA'].get('GENRES')
	os.environ['STAGES'] = config['DATA'].get('STAGES')
	os.environ['AGES'] = config['DATA'].get('AGES')
 
	# Adding ANTs and FSL to WSL .bashrc
	add_paths_to_bashrc(
		find_software_path('N4BiasFieldCorrection'), # ANTs bin path
		find_software_path('flirt') # FSL bin path
	)
