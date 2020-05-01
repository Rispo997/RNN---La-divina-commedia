from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import Dropout
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from pickle import dump
from utilities.plot import plot
import numpy as np
from keras.models import load_model
# To Do
# - Testare differenti tipi di architetture per la rete neurale (Layers,Activation function,dropout,batch size,epochs)
# - Testare differenti tipi di SEQUENCE_LEN
# - Valutare l'idea di eliminare le parole meno utilizzate
# - Valutare l'idea di un'approccio character-based

#Initialize parameters
SEQUENCE_LEN = 50 # The length of each sequence used to predict
STEP = 1 # Stride
X = [] # Input Variables 
Y = [] # Output Variables

# Open the file and encode newlines as standalone symbols
with open("resources/DC-poem-format.txt") as file:
    text = file.read().lower().replace('\n', ' \n ')
print('Number of Characters is:', len(text))

# Fetch all the words inside the file
words = []
padding_token = "_pad_"
start_token = "_start_"
for w in text.split(' '):
  if w.strip() != '' or w == '\n':
    if(w == start_token):
      for i in range(SEQUENCE_LEN-1):
        words.append(padding_token) 
    words.append(w)
print('Number of Words is:', len(words))


# Encode the words using integers
tokenizer = Tokenizer(filters=[], lower=True, oov_token="_unk_")
tokenizer.fit_on_texts(words)
words_tokenized = tokenizer.texts_to_sequences(words)
vocab_size = len(tokenizer.word_index) + 1
print('Number of Words is:', vocab_size)


# Flatten the resulting List
words_tokenized = [item for sublist in words_tokenized for item in sublist]

padding_token_val = words_tokenized[0]
start_token_val = words_tokenized[SEQUENCE_LEN-1]

n = 0
# Create Sequences
for i in range(SEQUENCE_LEN, len(words_tokenized), STEP):
  if words_tokenized[i] != padding_token_val and words_tokenized[i] != start_token_val:
    Y.append(words_tokenized[i])
    X.append(words_tokenized[i-(SEQUENCE_LEN):i])


X = np.array(X)
Y = np.array(Y)
Y = to_categorical(Y, num_classes=vocab_size)

# Create the neural network
model_filepath="weights.best.hdf5"
model = Sequential()
model.add(Embedding(vocab_size, 50, input_length=X.shape[1]))
model.add(LSTM(100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(100, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# Define Callbacks
es = EarlyStopping(monitor='accuracy', mode='max', verbose=1, patience=10)
ck = ModelCheckpoint(model_filepath, monitor='accuracy', verbose=1, save_best_only=True, mode='max')
# model = load_model('weights.hdf5')
# model.fit(X, Y, batch_size=128, epochs=38,callbacks=[es,ck,plot])
# Start Training
model.fit(X, Y, batch_size=128, epochs=100,callbacks=[es,ck,plot])
model.save('model.h5')
dump(tokenizer, open('tokenizer.pkl', 'wb'))