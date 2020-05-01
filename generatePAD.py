from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import numpy as np

def sample(preds, temperature=0.05):
      # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)

    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)
    
# # Initialize variables
text = '_start_'
print(text)
generated = []
n_words = 1000 
predicted_word = ''

# Load pre-trained data
model = load_model('models/weightsHLP-100-2.8770.hdf5')
tokenizer = load(open('models/tokenizerHighLevelPadding.pkl', 'rb'))
# Encode initial input
text_encoded = tokenizer.texts_to_sequences([text])[0]


while predicted_word != '_end_':
#for i in range(n_words):
    # Fix the length of the input sequence
    text_encoded = pad_sequences([text_encoded], maxlen=50, truncating='pre')
    # Get the model output
    prediction = model.predict(text_encoded, verbose=0)[0]
    # Sample and encode the output
    val = sample(prediction)
    output = np.array([val])
    predicted_word = tokenizer.sequences_to_texts([output])[0]
    generated.append(predicted_word)
    text_encoded = np.append(text_encoded[0], val)
    
    
# Format and print the result
generated = ['\n' if x=='_verse_' or x=='_end_' else x for x in generated]
output = ' '.join(generated)
print(*generated)
with open("output/seq50epoch100.txt", "w") as file:
	file.write(output)