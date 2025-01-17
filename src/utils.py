import os
import subprocess


def create_directory_if_not_exists(directory_path):
	"""
	Creates a directory if it does not exist.

	:param: directory_path: str, path to the directory.
	"""
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)


def convert_windows_path_to_wsl(windows_path):
	"""
	Converts a Windows file path to a WSL-compatible Linux file path.

	:param windows_path: str, the Windows file path to convert.
	:return: a WSL-compatible Linux file path.
	"""
	return windows_path.replace('C:\\', '/mnt/c/').replace('\\', '/')


def run_in_wsl(command):
	"""
	Runs a command intended for the WSL environment from Windows.

	:param command: list, the WSL command to run.
	:return: standard output from the command.
	"""
	wsl_command = ['wsl', 'bash', '-lic'] + [' '.join(command)]
	
	return subprocess.run(wsl_command, capture_output=True, text=True)


def find_software_path(software_name):
	"""
	Finds the installation path of a software using 'which' command within WSL.
	
	:param: software_name: str, name of the software to locate.
	:return: str, directory path where the software is located, or None if not found.
	"""
	try:
		result = run_in_wsl(['which', software_name])

		if result.returncode == 0:
			return '/'.join(result.stdout.strip().split('/')[:-1])
		else:
			print(f"Error locating {software_name}: {result.stderr.strip()}")
	except Exception as e:
		print(f"Error occurred during locating {software_name}: {e}")

	return None


def add_paths_to_bashrc(ants_bin_path, fsl_bin_path):
	"""
	Adds ANTs and FSL paths to the .bashrc file if they are not already present.
	
	:param: ants_bin_path: str, the path to the ANTs installation bin directory.
	:param: fsl_bin_path: str, the path to the FSL installation bin directory.
	"""
	try:
		bashrc_path = os.path.expanduser('~/.bashrc')
		new_lines = [
			f'export ANTSPATH={ants_bin_path}' if ants_bin_path else "",
			f'export FSLDIR={fsl_bin_path}' if fsl_bin_path else "",
			'PATH=$PATH:$ANTSPATH:$FSLDIR/bin',
			'export PATH'
		]
		new_lines = [line for line in new_lines if line]  # filter out empty strings

		with open(bashrc_path, 'a') as bashrc:
			for line in new_lines:
				bashrc.write(f"{line}\n")
		
		run_in_wsl(['source ~/.bashrc'])

	except Exception as e:
		print(f"An error occurred while updating .bashrc: {e}")
