from flask import Flask, request,render_template
import tensorflow as tf
from tensorflow import keras
import numpy as np 
from PIL import Image
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict' ,methods=['POST','GET'])

def function():
    class_names= ['adidas', 'converse', 'nike']
    img_height = 180
    img_width = 180
    model = tf.keras.models.load_model('model.hdf5')
    data= request.files['data']
    image = Image.open(data)
    image = image.resize((img_height, img_width))

    img_array = tf.keras.utils.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    classe_name = class_names[np.argmax(score)]
    score = round(100 * np.max(score),2)

    
    return render_template('index.html', score=score, classe_name=classe_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)