from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from gensim.models.wrappers import FastText


import fasttext
model = fasttext.train_unsupervised(input='utilities/DC-poem-formatLower.txt', minn=3, maxn=6, dim=100, epoch=20)
text_encoded = []
# Initialize variables
array_zero = np.array([0]*100)

for i in range(49):
	text_encoded.append([0]*100)
text_encoded.append(model['_start_'])
text_encoded = [text_encoded]
text_encoded = np.array(text_encoded).reshape(1, 50, 100)
#print(text_encoded)
print(text_encoded.shape)

generated = []
n_words = 2000  
predicted_word = ''

# Load pre-trained data
model = load_model('models/modelTry.h5')
tokenizer = load(open('models/tokenizer.pkl', 'rb'))

#text_encoded = tokenizer.texts_to_sequences([text])[0]

# Open the file and encode newlines as standalone symbols
with open("utilities/DC-poem-formatLower.txt", encoding='latin-1') as file:
    text = file.read().lower()

# Fetch all the words inside the file
words = []
words = [w for w in text.split(' ') if w.strip() != '' or w != '\n']
print('The length of the text:', len(words))

vocab_size = len(set(words))
tokens = list(set(words))


#while predicted_word != '_end_':
for i in range(n_words):
    # Fix the input sequence's length and predict the word
    #text_encoded = pad_sequences([text_encoded], maxlen=50, truncating='pre')
    output = model.predict_classes(text_encoded, verbose=0)
    # Translate the predicted word and add it to the result
    #predicted_word = tokenizer.sequences_to_texts([output])[0]
    #print(output)
    predicted_word = tokens[output[0]]
    generated.append(predicted_word)
    # Update the input text for next prediction
    text_encoded = np.append(text_encoded[0],output)
    if predicted_word == '_end_':
    	break
    
# Format and print the result
generated = ['\n' if x=='_verse_' or x=='_end_' else x for x in generated]
output = ' '.join(generated)
print(*generated)
with open("output/canto.txt", "w") as file:
	file.write(output)