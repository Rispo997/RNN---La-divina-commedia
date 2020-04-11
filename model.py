from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import Dropout
import numpy as np
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
with open("DC-modified.txt", encoding='utf-8') as file:
    text = file.read().lower().replace('\n', ' \n ')
print('Number of Characters is:', len(text))

# Fetch all the words inside the file
words = [w for w in text.split(' ') if w.strip() != '' or w == '\n']
print('Number of Words is:', len(words))
print(words[:100])

# Encode the words using integers
tokenizer = Tokenizer(filters=[])
tokenizer.fit_on_texts(words)
words_tokenized = tokenizer.texts_to_sequences(words)
vocab_size = len(tokenizer.word_index) + 1
print('Number of Words is:', vocab_size)

# Flatten the resulting List
words_tokenized = [item for sublist in words_tokenized for item in sublist]
print(words_tokenized[3000:3005])

# Create Sequences
for i in range(0, len(words_tokenized) - SEQUENCE_LEN, STEP):
    X.append(words_tokenized[i: i + SEQUENCE_LEN])
    Y.append(words_tokenized[i + SEQUENCE_LEN])
print('Number of Sequences:', len(X))
X = np.array(X)
Y = np.array(Y)
Y = to_categorical(Y, num_classes=vocab_size)
# Create the neural network
model = Sequential()
model.add(Embedding(vocab_size, 50, input_length=X.shape[1]))
model.add(LSTM(100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(100, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))
print(model.summary())
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, batch_size=128, epochs=100)
