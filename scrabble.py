


from wordscore import score_word
import string
import sys
import re


def loaddata():
    '''
    this func is to load data from sowpods
    '''
    with open("sowpods.txt","r") as infile:
        raw_input = infile.readlines()
        data = [datum.strip('\n') for datum in raw_input]
        return data


def can_form_word(rack_letters, word):
    """
    Determine whether a word can be formed only using the letters on the rack.
    """   
    return all(word.count(c) <= rack_letters.count(c) for c in word)


def valid_word(input_word):
    '''
    Returns valid words from the text file as a list
    '''
    illegal_characters = '0123456789!#$%&()+,-\./:;@[\\]^_`{|}~'
    data = [x for x in loaddata() if len(x) <= 7]
    if input_word.isalpha() == False:
        rm_illegal = [i.replace(illegal_characters,'').upper() for i in input_word]
        v_word = [word for word in data if can_form_word(rm_illegal, word)] 
    else:    
        v_word = [word for word in data if can_form_word(input_word.upper(), word)] 
    return list(filter(lambda x: x, v_word))

def wildcards(input_word):
    '''To handle inputs with wildcard characters'''
    
    remove_wild = input_word.replace('?','').replace('*','')
    words = valid_word(remove_wild)
    words_scores = [(score_word(word),word.lower()) for word in words]

    n = len(words)
    
    if '?' in input_word:
        for letter in list(string.ascii_uppercase):
            score_letter = score_word(letter)
            new_word = input_word.replace('?',letter)
            if '*' in input_word:
                for next_letter in list(string.ascii_uppercase):
                    new_word = input_word.replace('?',letter).replace('*',next_letter)
                    score_next_letter = score_letter + score_word(next_letter)
                    word_set_list = [(score_word(word)-score_next_letter,word.lower()) for word in valid_word(new_word) if word not in words]
                    words.extend(valid_word(new_word))
                    words=list(set(words))
                    words_scores.extend(word_set_list)
            else:
                words_scores.extend([(score_word(word)-score_letter,word.lower()) for word in valid_word(new_word) if word not in words])
                words.append(new_word)
        return words_scores
    elif '*' in input_word:
        for letter in list(string.ascii_uppercase):
            score_letter = score_word(letter)
            new_word = input_word.replace('*',letter)
            words_scores.extend([(score_word(word)-score_letter,word.lower()) for word in valid_word(new_word) if word not in words])
        return words_scores

  
    
def run_scrabble(input_word):
    '''
    To run scrabble function
    '''

    if len(input_word) < 2:
        return "Invalid input: number of characters must be greater than 2."
    elif len(input_word) > 7:
        return "Invalid input: number of characters must be less than 7."

    elif (input_word.count('?') > 1) or  (input_word.count('*') > 1):

        return "Too many wild card character, only 1 allowed."

        
    else:
        if re.findall('[A-Z]*[\?\*]+[A-Z]*',input_word):
            words_scores = wildcards(input_word)
        else:           
            words_scores = [(score_word(word), word.lower()) for word in valid_word(input_word)]




        words_scores = sorted(words_scores, key = lambda x : x[1]) # first sorting the words in alphabetical order
        words_scores = sorted(words_scores, key = lambda x : x[0], reverse=True) # then sorting the word score in descending order
        return [(point, word.upper()) for point, word in words_scores] , len(words_scores)


# input_word = "ABC"
# # input_word = 'ABC*'
# run_scrabble(input_word)
# valid_word(input_word)
# wildcards(input_word)
