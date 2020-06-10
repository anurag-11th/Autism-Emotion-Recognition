from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty, StringProperty  # pylint: disable=E1136
from kivy.core.window import Window
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re
import random
import ntpath
import os
import subprocess
import sys
from glob import glob as gb
from processFiles import splitFile
from model import predict
from output import drawResults


ACCEPTED_FILES = r'(\.mp4)|(\.avi)'
DIR_PATH = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
FEATURE_EXTRACTOR = DIR_PATH + "/extractor/FeatureExtraction.exe"
OUT_DIR = DIR_PATH + "/features/"
EMOTION_LABELS = ['Curious', 'Engaged', 'Joy', 'Neutral', 'Surprised', 'Uncomfortable']


def generateUniqueCode(max=10000):
    """
        Generate a unique code for the video being processed.
        ------------------------------------------------------
        Arguements:
            max: The upper limit to generate a unique code.
    """

    return str(random.randint(0, max))


def getFileName(path):
    """
        Generate the name of the video file from the filepath.
        ------------------------------------------------------
        Arguements:
            path: path to the file from which the name is to be extracted.
        ------------------------------------------------------
        Returns:
            tail: The filename extracted from the file path.
    """

    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def generateErrorBox(error):
    """
        Generate an error box with the given error message.
        ------------------------------------------------------
        Arguements:
            error: Error message to be shown
    """

    lyt = BoxLayout(orientation='vertical')
    lbl = Label(text=error, size_hint=(1, 0.3), font_size=25)
    btn = Button(text="Close", size_hint = (1, 0.2))
    lyt.add_widget(lbl)
    lyt.add_widget(btn)
    popup = Popup(title="Error!", content=lyt, size_hint=(None, None), size=(400, 400))
    btn.bind(on_press=popup.dismiss)
    popup.open()
    return


if not os.path.isfile(FEATURE_EXTRACTOR):
    ER_TXT = """OpenFace library has not been installed in the 'extractor' directory. \
                For more details, refer to the installation guide. \
             """
    generateErrorBox(ER_TXT)

if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)
    

class Manager(ScreenManager):

    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    # screen_three = ObjectProperty(None)
    # screen_four = ObjectProperty(None)


class UploadScreen(Screen):

    def clear_upload(self):
        self.ids.upload_space.text = ""

    def upload(self):
        Tk().withdraw()                         # We don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()            # Show an "Open" dialog box and return the path to the selected file
        self.ids.upload_space.text = str(filename)
        # pass

    def upload_process(self):
        
        filepath = self.ids.upload_space.text
        print(filepath)

        # Raise an error in case if no file is chosen
        if filepath == "":
            generateErrorBox("No file is chosen")

        # Check if the file entered is of the supported type
        elif re.search(ACCEPTED_FILES, filepath):

            name = getFileName(filepath)
            ind = re.search(ACCEPTED_FILES, name)
            directory = name[:ind.start()] + '-' + generateUniqueCode()
            new_dir = os.path.join(OUT_DIR, directory)  # Parent directory where the features are stored

            # Make a new directory where the extracted features are stored.
            try:  
                os.mkdir(new_dir)  
            except OSError as error:  
                generateErrorBox(str(error))

            # Extract features using OpenFace Library
            res = subprocess.run([FEATURE_EXTRACTOR, '-f', filepath, '-out_dir', new_dir])

            # New changes to be made to the above section
            # try:
            #     res = subprocess.run([FEATURE_EXTRACTOR, '-f', filepath, '-out_dir', new_dir])
            # except FileNotFoundError as err:
            #     print(err)


            # If shell command has been executed successfully
            if res.returncode == 0:
                print("Saved to: {}".format(new_dir))
                l = gb(new_dir + '/*')

                if len(l) == 0:
                    generateErrorBox("Looks like something is wrong. The given file could not be processed.")
                
                else:
                    features_file = gb(new_dir + '/*.csv')[0].replace('\\', '/')
                    splits = splitFile(features_file, new_dir)

                    if splits['ignored'] == True:
                        generateErrorBox(splits['message'])
                    
                    else:
                        result = predict(splits['data'])
                        out_video = gb(new_dir + '/*.avi')[0].replace('\\', '/')

                        if result['success'] == True:
                            dr_result = drawResults(out_video, result['predictions'])

                            if dr_result['message'] != None:
                                generateErrorBox(dr_result['message'])

                            else:
                                print('Labelled ouput can be seen at: {}\n'.format(dr_result['outfile']))
                                self.manager.current = "Screen2"
                                self.manager.screens[1].video_file.source = dr_result['outfile']
                                self.manager.screens[1].video_file.state = 'play'

                        else:
                            generateErrorBox(result['message'])


            else:
                err_msg = "Feature extraction could not be done successfully on the given file."
                generateErrorBox(err_msg)

        else:
            file_error_text = """Looks like the file type uploaded is not supported. \
                                 Currently, the accepted file types are .mp4 and .avi. \
                                 Please try another file.\
                              """
            generateErrorBox(file_error_text)


class ResultScreen(Screen):

    video_file = ObjectProperty(None)


class ScreenApp(App):

    def build(self):
        self.title = 'AER: Autism Emotion Recognition'
        return Manager()

if __name__.endswith('__main__'):
    ScreenApp().run()
    # time.sleep(15)