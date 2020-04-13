from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import numpy as np

# Initialize variables
text = 'Rispuosemi Non omo omo già fui _verse_ e li parenti miei furon lombardi'
generated = []
n_words = 500  
predicted_word = ''

# Load pre-trained data
model = load_model('models/model.h5')
tokenizer = load(open('models/tokenizer.pkl', 'rb'))

text_encoded = tokenizer.texts_to_sequences([text])[0]

while predicted_word != '_end_':
#for i in range(n_words):
    # Fix the input sequence's length and predict the word
    text_encoded = pad_sequences([text_encoded], maxlen=20, truncating='pre')
    output = model.predict_classes(text_encoded, verbose=0)
    # Translate the predicted word and add it to the result
    predicted_word = tokenizer.sequences_to_texts([output])[0]
    generated.append(predicted_word)
    # Update the input text for next prediction
    text_encoded = np.append(text_encoded[0],output)
    
# Format and print the result
generated = ['\n' if x=='_verse_' else x for x in generated]
print(*generated)