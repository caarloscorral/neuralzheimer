
# NeurAlzheimer Project

NeurAlzheimer leverages Deep Learning techniques to detect the stages of Alzheimer's disease using MRI brain images in NiFTI format.
This project focuses on pre-processing medical imaging data, extracting meaningful features, and training models to classify the progression of Alzheimer's disease.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Requirements

This project is built with Python and requires specific packages to function correctly. The key dependencies are listed below:

- Python 3.8+
- TensorFlow 2.10.0
- Keras 2.10.0
- ANTsPyx 0.5.4
- NiBabel 5.3.2
- Scikit-Learn 1.5.2
- SciPy 1.13.1
- And more included in `requirements.txt`

For the full list of dependencies, see the [requirements.txt](requirements.txt) file.

---

## Installation

To set up the project in your local environment, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/caarloscorral/neuralzheimer.git
   ```

2. Navigate to the project directory:
   ```bash
   cd neuralzheimer
   ```

3. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On MacOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the project dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Project Structure

The project is organized into several key directories and files:

```
neuralzheimer/
│
├── src/
│   └── create_env.py
│   ├── data_manager.py
│   ├── feature_extractor.py
│   ├── main.py
│   ├── model_trainer.py
│   └── preprocessor.py
|
├── config.ini
├── requirements.txt
└── README.md
```

- **`config.ini`**: Contains configuration settings for environment paths and data classifications.
- **`src/create_env.py`**: Sets up environment configurations and paths.
- **`src/data_manager.py`**: Handles data extraction from zip files and conversion from DICOM to NIfTI formats.
- **`src/feature_extractor.py`**: Defines methods to compute features from processed images.
- **`src/main.py`**: Main execution script to handle data pre-processing and model training.
- **`src/model_trainer.py`**: Contains classes and methods for building and training the CNN model.
- **`src/preprocessor.py`**: Pre-processes MRI images through various stages including normalization, registration, and skull stripping.

---

## Usage

1. **Data Pre-processing and Feature Extraction:**

   The main processing steps include skull stripping, alignment, registration, and normalization of MRI images. Execute `src/main.py` to run these processes and extract features for model training.

2. **Model Training and Classification:**

   Train a neural network model using extracted features and segmented MRI images to classify Alzheimer's disease stages.

---

## Contributing

Contributions are welcomed! If you have suggestions or improvements for the project, feel free to fork the repository, make your changes, and submit a pull request. Please ensure your contributions adhere to the project's coding standards.

---

## License

This project is licensed under the MIT License - see the [LICENSE] (https://github.com/caarloscorral/neuralzheimer/blob/main/LICENSE) file for details.
