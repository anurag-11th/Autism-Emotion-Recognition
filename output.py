import re
import cv2
import ntpath
import traceback
# import numpy as np
from math import ceil
# import face_recognition
from processFiles import getFileName

# face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_alt2.xml')
EMOTION_LABELS = ['Curious', 'Engaged', 'Joy', 'Neutral', 'Surprised', 'Uncomfortable']

def getFileBase(path):
    """
        Get the parent directory of the give file.
        ------------------------------------------------------
        Arguements:
            path: path to the file from which the directory is to be found.
        ------------------------------------------------------
        Returns:
            head: The parent directory path.
    """
    head, _ = ntpath.split(path)
    return head


def drawResults(path, predictions):

    res = {'outfile': None,
            'message': None}

    try:
        cap = cv2.VideoCapture(path)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        splits = ceil(length / 30)

        in_file = getFileName(path)
        x = re.search(r'\.', in_file)
        sub = in_file[:x.start()]
        out_file = getFileBase(path) + '/' + sub + '-labelled.avi'

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(out_file, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

        # Font settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 2
        thick = 3
        glow = 3 * thick

        # Color settings
        black = (0, 0, 0)
        white = (255, 255, 255)
        yellow = (0, 255, 255)
        red = (0, 0, 255)

        # frames = []
        frame_count = 0
        i = 0
        

        while 1:
            ret, frame = cap.read()

            if not ret:
                break
            
            x = 5
            y = int(1920/2) + 225
            w = int(frame.shape[1]* 0.3)

            text = 'Emotions'
            size, _ = cv2.getTextSize(text, font, scale, thick)
            y += size[1] + 20

            cv2.putText(frame, text, (x, y), font, scale, black, glow)
            cv2.putText(frame, text, (x, y), font, scale, yellow, thick)

            y += 20
            cv2.line(frame, (x,y), (x+w,y), black, 7)

            size, _ = cv2.getTextSize('happiness', font, scale, thick)
            t = int(1.5 * (size[0] + 20))
            w = 350
            h = size[1]
                    
            if (frame_count % 30 == 0) & (i < splits):
                current_preds = list(predictions[i])
                bigger = EMOTION_LABELS[current_preds.index(max(current_preds))]
                i += 1

            for l, v in zip(EMOTION_LABELS, current_preds):
                lab = '{}:'.format(l)
                val = '{:.2f}'.format(v)
                size, _ = cv2.getTextSize(l, font, scale, thick)

                # Set a red color for the emotion with bigger probability
                color = red if l == bigger else yellow

                y += size[1] + 35

                p1 = (x+t, y-size[1]-5)
                p2 = (x+t+w, y-size[1]+h+5)
                cv2.rectangle(frame, p1, p2, black, 6)

                # Draw the filled rectangle proportional to the probability
                p2 = (p1[0] + int((p2[0] - p1[0]) * v), p2[1])
                cv2.rectangle(frame, p1, p2, color, -1)
                cv2.rectangle(frame, p1, p2, black, 4)

                # Draw the emotion label
                cv2.putText(frame, lab, (x, y), font, scale, black, glow)
                cv2.putText(frame, lab, (x, y), font, scale, color, thick)

                # Draw the value of the emotion probability
                cv2.putText(frame, val, (x+t+15, y), font, scale, black, glow)
                cv2.putText(frame, val, (x+t+15, y), font, scale, white, thick)
            
            frame_count += 1
            print("Writing frame {} / {}".format(frame_count, length))
            out.write(frame)
                
            # k = cv2.waitKey(30) & 0xff
            # if k == 27:           # ESC Key
            #     break

        cap.release()
        cv2.destroyAllWindows()

        res['outfile'] = out_file
        # res['message'] = "Success!"

        return res

    except Exception as e:
        res['message'] = str(e)
        traceback.print_tb(e.__traceback__)
        return res
