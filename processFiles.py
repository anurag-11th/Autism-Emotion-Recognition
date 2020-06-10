import os
import re
import ntpath
import numpy as np
import pandas as pd
from math import ceil

REQ_COLS = ['gaze_0_x', 'gaze_0_y', 'gaze_0_z', 'gaze_1_x', 'gaze_1_y', 'gaze_1_z', 'gaze_angle_x', 
            'gaze_angle_y', 'pose_Tx', 'pose_Ty', 'pose_Tz', 'pose_Rx', 'pose_Ry', 'pose_Rz', 'AU01_r', 'AU02_r', 'AU04_r',
            'AU05_r', 'AU06_r', 'AU07_r', 'AU09_r', 'AU10_r', 'AU12_r', 'AU14_r', 'AU15_r', 'AU17_r', 'AU20_r', 'AU23_r', 
            'AU25_r', 'AU26_r', 'AU45_r', 'AU01_c', 'AU02_c', 'AU04_c', 'AU05_c', 'AU06_c', 'AU07_c', 'AU09_c', 'AU10_c',
            'AU12_c', 'AU14_c', 'AU15_c', 'AU17_c', 'AU20_c', 'AU23_c', 'AU25_c', 'AU26_c', 'AU28_c', 'AU45_c']

AU_PRESENCE = ['AU01_c', 'AU02_c', 'AU04_c', 'AU05_c', 'AU06_c', 'AU07_c', 'AU09_c', 'AU10_c', 'AU12_c', 'AU14_c', 
              'AU15_c', 'AU17_c', 'AU20_c', 'AU23_c', 'AU25_c', 'AU26_c', 'AU28_c', 'AU45_c']

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


def splitFile(file, out_folder, count=30, minf=15):

    """
        Split the total frames into 1 second divisions.
        ------------------------------------------------------
        Arguements:
            file: The .csv file to be split.
            out_folder: The parent folder in which a new folder called split
                        is created to store the split files.
            count: The number of frames to divide on. Default is 30.
            minf: The minimum number of frames that should be considered.
                  Default is 15.
        ------------------------------------------------------
        Returns:
            out: A dictionary object which has the following 3 properties:
                data: A list which contains the location to the split files.
                      Default is None.
                ignored: Whether the given file is ignored or not. Default is False.
                message: Error message in case of an error.

    """

    # dat = pd.DataFrame(columns=['File Name', 'Emotion'])
    split_files = []
    out = {'data': None,
            'ignored': False,
            'message': None}
    
    dr = pd.read_csv(file)
    frame_count = dr.shape[0]
    dr.columns = [col.strip() for col in dr.columns]
    dr = dr[dr['confidence'] > 0]
    dr = dr[REQ_COLS]
    dr[AU_PRESENCE] = dr[AU_PRESENCE].astype('category')
    
    if frame_count == 0:
        out['ignored'] = True
        out['message'] = 'Ignored file: {} because of zero frames. \n'.format(file)
        return
        
    elif frame_count < minf:
        out['ignored'] = True
        out['message'] = 'Ignored file: {} because of insufficient frames: {}. \n'.format(file, frame_count)
        return
        
    print("No. of frames in {}: {}".format(file, frame_count))
    no_splits = ceil(frame_count / count)
    
    filename = getFileName(file)
    x = re.search(r'\.', file)
    sub = filename[:x.start()]

    out_dir = os.path.join(out_folder+'/', 'split')
    os.mkdir(out_dir)

    for i in range(no_splits):
        dt = dr.loc[i*count:i*count+(count-1), :]
        new_file = out_dir + '/' + sub + '-' + str(i) + '.csv'
        row_ct = dt.shape[0]
        if row_ct == count:
            dt.to_csv(new_file, index=False)
            split_files.append(new_file)
        elif row_ct < count:
            no_req = count - row_ct
            l = np.zeros(shape=(no_req, dt.shape[1]))
            dt = dt.append(pd.DataFrame(l, columns=dt.columns))
            dt.to_csv(new_file, index=False)
            split_files.append(new_file)

        print("File has been saved to: {}".format(new_file))
    print()

    out['data'] = split_files


    return out