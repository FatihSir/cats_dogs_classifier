from flask import Flask, render_template, request, url_for
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import keras

model_path = 'cats_and_dogs_small_4.h5'
model = keras.saving.load_model(model_path)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def predict():
    imagefile = request.files['imagefile']
    if imagefile:
        image_path = "./static/images/" + imagefile.filename
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        imagefile.save(image_path)
        image = load_img(image_path, color_mode='rgb', target_size=(150, 150))
        image = img_to_array(image)
        im = image.reshape(1, 150, 150, 3)
        im = im / 255.0

        class_names = {0: 'cat', 1: 'dog'}
        prediction = model.predict(im).astype('int')
        predicted_class = class_names[prediction[0][0]]
        classification = f'This is a {predicted_class}'
        image_url = url_for('static', filename='images/' + imagefile.filename)
    else:
        classification = 'No image uploaded.'
        image_url = None

    return render_template('index.html', prediction=classification, image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
