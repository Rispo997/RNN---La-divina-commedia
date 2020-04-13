import numpy as np
import unidecode

def evaluateText(filepath='../output/canto.txt'):
    score = dict()
    result = list()
    comparisons = 0
    with open(filepath) as dc:
        lines = list(line for line in (l.strip() for l in dc.readlines()) if line)  # Remove lines with only newline
        words_per_line = [len(line) for line in lines]
        score['mean'] = np.mean(words_per_line)
        score['variance'] = np.var(words_per_line)
        sentences = [line for line in lines if 'Canto' not in line]
        # Compare lines, the rhymes must be of the form: ABA BCB 
        for i in range(0,len(sentences)-3,3):
            result.append(check_rime(sentences[i],sentences[i+2])) # Compare A - A
            result.append(check_rime(sentences[i+1],sentences[i+3])) # Compare B - B
            comparisons += 2
        score['rhymes'] = sum(result)/comparisons # Normalize result
        print(score)
        
def check_rime(first,second):
    return last_syll(first) == last_syll(second)
    

def last_syll(word):
    vowels = ['a','e','i','o','u']
    word = unidecode.unidecode(word)
    for i in reversed(range(len(word)-1)):
        if word[i] in vowels:
            return word[i+1:]
        
        
evaluateText()


