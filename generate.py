from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import fasttext
from scipy.ndimage.interpolation import shift
from scipy import spatial
from gensim.models import fasttext
import fasttext as FT
#Model = fasttext.train_unsupervised(input='utilities/DC-poem-formatUTF.txt', minn=3, maxn=6, dim=100, epoch=20)
#text_encoded = []

Model = fasttext.load_facebook_vectors("utilities/embeddings.bin", encoding='utf-8')

# Initialize variables
for i in range(49):
	text_encoded.append([0]*100)
text_encoded.append(Model['_start_'])
text_encoded = [text_encoded]
print(len(text_encoded[0][0]))
text_encoded = np.array(text_encoded).reshape(1, 50, 100)
print(text_encoded.shape)

generated = []
n_words = 500
predicted_word = ''

# Load pre-trained data
model = load_model('models/modelFTVector100Epoch.h5')
tokenizer = load(open('models/tokenizer.pkl', 'rb'))
#Luca's old but gold generate.py
# def sample(preds, temperature=0.01):
#      # helper function to sample an index from a probability array
#     preds = np.asarray(preds).astype('float64')
#     preds = np.log(preds) / temperature
#     exp_preds = np.exp(preds)
#     preds = exp_preds / np.sum(exp_preds)

#     probas = np.random.multinomial(1, preds, 1)
#     return np.argmax(probas)
    
# # Initialize variables
# text = '_pad_ '*49 + ' _start_ '
# print(text)
# generated = []
# n_words = 1000 
# predicted_word = ''

# # Load pre-trained data
# model = load_model('weights-100-2.8770.hdf5')
# tokenizer = load(open('tokenizer.pkl', 'rb'))


# Ho nascosto il codice in una funzione perchè mi vergognavo
def process_sequence(old_seq,new_value):
    # Crea un nuovo vettore contenente tutte le parole dalla seconda all'ultima
    new_seq = []
    for word in old_seq[0][1:]:
        encoding = []
        for n in word:
            encoding.append(n)
        new_seq.append(encoding)
    # Inserisci la nuova parola e sistema la dimensione
    new_seq.append(new_value)
    new_seq = [new_seq]
    new_seq = np.array(new_seq).reshape(1, 50, 100)
    return new_seq


    
#text_encoded = tokenizer.texts_to_sequences([text])[0]

# Open the file and encode newlines as standalone symbols
with open("utilities/DC-poem-formatUTF.txt", encoding='latin-1') as file:
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
    #Categorical FastText
    #output = model.predict_classes(text_encoded, verbose=0)
    output = model.predict(text_encoded, verbose=0)[0]
    
    #Luca is bull, despite me
    #prediction = model.predict(text_encoded, verbose=0)[0]
    #val = sample(prediction)
    #output = np.array([val])
    #---------------------

	# Translate the predicted word and add it to the result
    #predicted_word = tokenizer.sequences_to_texts([output])[0]
    #print(output)
    
    #Categorical FastText
    #predicted_word = tokens[output[0]]
    #text_encoded = process_sequence(text_encoded,Model[predicted_word])
    
    
    predicted_word = Model.similar_by_vector(output, topn = 1)[0][0]

    #words = Model.get_words()
    # min = spatial.distance.cosine(output, Model[words[0]])
    # id_min = 0
    # for i in range(1, len(words)):
    #     cs = spatial.distance.cosine(output, Model[words[i]])
    #     if  cs < min:
    #         min = cs
    #         id_min = i 

    # predicted_word = words[id_min]
    if i < 20:
        print(output)
        print(" => ")
        print(predicted_word)
    text_encoded = process_sequence(text_encoded,Model[predicted_word])

    generated.append(predicted_word)
    # Update the input text for next prediction
    if predicted_word == '_end_':
    	break

    #Luca's old but gold
    #text_encoded = np.append(text_encoded[0],sample(prediction))
    
# Format and print the result
generated = ['\n' if x=='_verse_' or x=='_end_' else x for x in generated]
output = ' '.join(generated)
print(*generated)
with open("output/cantoFT.txt", "w") as file:
	file.write(output)