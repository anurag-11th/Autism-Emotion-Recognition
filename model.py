import numpy as np
import pandas as pd
import tensorflow as tf

MODEL  = tf.keras.models.load_model('models/model1.h5')

def predict(files):
    data = {'predictions': None,
            'success': False,
            'message': None}

    x_te = []
    for i in files:
        x_te.append(pd.read_csv(i).values)

    x_pred = np.array(x_te, ndmin=3)

    if (x_pred.shape[1] == 30) & (x_pred.shape[2] == 49):  # pylint: disable=E1136  # pylint/issues/3139
        y_pred = MODEL.predict(x_pred)
        data['predictions'] = y_pred
        data['success'] = True
        data['message'] = 'Predictions have been made successfully.'

    else:
        data['success'] = False
        data['message'] = 'Error due to the dataset having a shape of {} when expected shape is (?, 30, 49).'.format(x_pred.shape)
    
    return data