# Autism-Emotion-Recognition
An application to predict the emotions being shown by an individual with Autism Spectrum Disorder.


## Installation Guide

1. Download the repository and extract it into a directory of your choosing. For guidance purposes, let us consider the name of this directory to be 'application'.

2. Download the OpenFace library from the [given link](https://github.com/TadasBaltrusaitis/OpenFace/releases/download/OpenFace_2.2.0/OpenFace_2.2.0_win_x86.zip "OpenFace installation") for Windows. Extract the contents into a directory called 'extractor' in the 'application' directory. The path to FeatureExtraction.exe should look similar to this: "../application/extractor/FeatureExtraction.exe"

   For other platforms, refer to the [wiki](https://github.com/TadasBaltrusaitis/OpenFace/wiki) on how to install. The FeatureExtraction command should be in the 'extractor' directory.

3. Create a virtual environment of Python 3.6 or above using virtualenv or Anaconda and install the required packages for the application using the command: `pip install -r requirements.txt`.

4. Execute the following command to run the application: `$ python main.py`

5. Select the file to be processed by clicking on the Select button. Click on Evaluate to process the file. Only .mp4 or .avi files are currently supported.

6. Click on Reset to evaluate another file.
