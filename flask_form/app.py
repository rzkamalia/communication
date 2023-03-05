from flask import Flask, render_template, request
import tensorflow
import numpy as np
import pandas as pd

# example input: 
# Shell and BG Shareholders to Vote on Deal at End of January 

label_map = {0: 'positive', 1: 'negative', 2: 'neutral'}

def processAI(inputS):
    # preprocessing 
    tokenizer = tensorflow.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(inputS)
    sequences = tokenizer.texts_to_sequences(inputS)

    # input sentence to model 
    model = tensorflow.keras.models.load_model('best_nlp.h5')
    pred = model.predict(sequences)
    pred = np.argmax(pred, axis = 1)
    pred = label_map[pred[0]]
    return pred

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        sentence = request.form['sentence']
        return render_template('result.html', sentiment = processAI([sentence]))
    return render_template('form.html')

app.run()