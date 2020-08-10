from flask import Flask,request, jsonify, json
from flask_cors import CORS
from io import BytesIO
import json
import base64
from PIL import Image
import numpy as np
from keras.models import model_from_json
import tensorflow as tf
from tensorflow import keras
from sendAlert import send_msg,send_email
app = Flask(__name__)
CORS(app)

# Loading the model
loaded_model_1 = keras.models.load_model('model')
labels=['fire', 'neutral', 'smoke']

IMAGE_SIZE=128
################################################################################################
## Model testing
# img = tf.keras.preprocessing.image.load_img('ggb.jpg', target_size=(IMAGE_SIZE, IMAGE_SIZE))
#returns A PIL Image instance

# x = tf.keras.preprocessing.image.img_to_array(img,data_format='channels_last', dtype='float32')/255
# test_img = x.reshape(1,IMAGE_SIZE, IMAGE_SIZE,3)
# tf_model_predictions=loaded_model_1.predict(test_img)
# predicted_ids = np.argmax(tf_model_predictions)
# predicted_labels = labels[predicted_ids]
# print('prediction ',predicted_labels)

# img = tf.keras.preprocessing.image.load_img('fire.jpg', target_size=(IMAGE_SIZE, IMAGE_SIZE))
# x = tf.keras.preprocessing.image.img_to_array(img,data_format='channels_last', dtype='float32')/255
# print(x.shape)
# test_img = x.reshape(1,IMAGE_SIZE, IMAGE_SIZE,3)
# tf_model_predictions=loaded_model_1.predict(test_img)
# predicted_ids = np.argmax(tf_model_predictions)
# predicted_labels = labels[predicted_ids]
# print('prediction ',predicted_labels)
################################################################################################

def get_PIL(base64_data):
    im_bytes = base64.b64decode(base64_data)   # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    return Image.open(im_file)   # img is now PIL Image object

def predict_result(PIL_Image):
    newImage=PIL_Image.resize((IMAGE_SIZE,IMAGE_SIZE))
    x1 = tf.keras.preprocessing.image.img_to_array(newImage,data_format='channels_last', dtype='float32')/255
    print(x1.shape)
    test_img1 = x1.reshape(1,IMAGE_SIZE, IMAGE_SIZE,3)
    tf_model_predictions1=loaded_model_1.predict(test_img1)
    predicted_ids1 = np.argmax(tf_model_predictions1)
    predicted_labels1 = labels[predicted_ids1]
    if(predicted_ids1==2 and tf_model_predictions1[0][2]<0.85):
        predicted_labels1=labels[1]
    return predicted_labels1

@app.route('/predict',methods=['GET', 'POST', 'DELETE', 'PUT'])
def predict():
    if request.method == 'GET':
        return jsonify({"error":"Yes"})
    elif request.method == 'POST':
        
        request_data=request.get_json()
        image_txt=request_data["image_txt"]
        
        image_txt=image_txt.split(",")[1]
        result=predict_result(get_PIL(image_txt))
        print(result)
        response=app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )
        return response

@app.route('/sendNotification',methods=['POST'])
def sendNotification():
    if request.method=='POST':
        request_data=request.get_json()
        if(request_data['email']):
            send_email(request_data['email'],90)
        if(request_data['mobile']):
            send_msg(request_data['mobile'],90)
        response=app.response_class(
            response=json.dumps('Notification Sent'),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/')
def isAppup():
    return "Application is up"

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=5000,debug = True)