import numpy as np
import unidecode

def evaluateText(filepath='../resources/DC-cleaned.txt'):
    score = dict()
    result = list()
    comparisons = 0
    with open(filepath,encoding="latin-1") as dc:
        lines = list(line for line in (l.strip() for l in dc.readlines()) if line)  # Remove lines with only newline
        c1 = [len(line) for line in lines]
        chars_per_line = [len(line) for line in lines if line.find("Canto") == -1]
        score['mean'] = np.mean(chars_per_line)
        score['variance'] = np.var(chars_per_line)
        sentences = [line for line in lines if 'Canto' not in line]
        # Compare lines, the rhymes must be of the form: ABA BCB CDC
        start = True
        #if we are not computing the entire DC, but just a canto
        entire_DC = False
        if lines[0].find("Canto") == -1:
            i = 2
        else:
            entire_DC = True
            i = 3
        while i < len(lines)-1:
            #check if a cantica is read and go to the next in the right point
            if entire_DC:
                for j in range(3):
                    if lines[i-j].find("Canto") != -1:
                       i += -j+3
                       start = True
            #if that's the first check of a cantica check A rhyme (only two verses)
            if start == True:
                result.append(check_rime(lines[i],lines[i-2])) # Compare all the rhymes should be equal to the current verse
                comparisons += 1
                start = False
                # if (not check_rime(lines[i],lines[i-2])):
                #     print(lines[i])
                #     print(lines[i-2])
                #     print("-----------------")
            #normal check for B in ABA BCB where i is positioned at the last B
            else:
                result.append(check_rime(lines[i],lines[i-2]) and check_rime(lines[i-2],lines[i-4])) # Compare all the rhymes should be equal to the current verse
                comparisons += 1
                # if (not (check_rime(lines[i],lines[i-2]) and check_rime(lines[i-2],lines[i-4]))):
                #     print(lines[i])
                #     print(lines[i-2])
                #     print(lines[i-4])
                #     print("-----------------")
            i+=3
        score['rhymes'] = result.count(True)/comparisons # Normalize result
        print(score)
        
def check_rime(first,second):
    #return last_syll(first) == last_syll(second)    I'm sorry man, I changed it ;)
    first_word = get_last_word(first)
    second_word = get_last_word(second)
    vowels = ['a','e','i','o','u']
    # chek last char
    if(first_word[-1] != second_word[-1]):
        return False
    i = 2
    #check if equal since the next vowel
    for n in range(min(len(first_word), len(second_word))-2):
        if (first_word[-i] != second_word[-i]):  
            return False
        elif (first_word[-i] in vowels):  
            return True      
        i += 1
    return True

#get the last verse's word normalized 
def get_last_word(verse):
    return verse.split()[-1].strip('’)').lower().replace('à', 'a').replace('è', 'e').replace('é', 'e').replace('ì', 'i').replace('ò', 'o').replace('ó', 'o').replace('ù', 'u')

#old implementation
def last_syll(word):
    vowels = ['a','e','i','o','u']
    word = unidecode.unidecode(word)
    for i in reversed(range(len(word)-1)):
        if word[i] in vowels:
            return word[i+1:]

print("DC: ")
evaluateText()
print("\nOur Model: ")
evaluateText("../output/seq50epoch100.txt")