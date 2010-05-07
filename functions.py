def print_to_file(numericalArray, labels):
    # Create file to save the output
    train_data = open('../matlab_data/train_data_tf.csv', 'w')    
    train_labels = open('../matlab_data/train_labels.csv', 'w')
    test_data = open('../matlab_data/test_data_tf.csv', 'w')
    test_labels = open('../matlab_data/test_labels.csv', 'w')
    
    # Print all the numerical data to the file
    for i in range(len(numericalArray)):
  
                if (i % 4) == 0:
                        test_data.write(str(numericalArray[i]).strip('[]'))
                        test_data.write('\n')
                        test_labels.write(str(labels[i]).strip('[]'))
                        test_labels.write('\n')
                else:
                        train_data.write(str(numericalArray[i]).strip('[]'))
                        train_data.write('\n')
                        train_labels.write(str(labels[i]).strip('[]'))
                        train_labels.write('\n')

                
        #labelsMatlab.write(labels[lineno])
        #dataMatlab.write('\n')

def parse_url(sentence):
    wordsToAdd = []
    wordsToDelete = []
    for word in sentence:
        if word[0:4] == 'http':
            urlInfo = word.split('/')
            try:
                #print word
                #print urlInfo[2].strip('www.').split('.')[0]
                wordsToAdd.append(urlInfo[2].strip('www.').split('.')[0])
                wordsToDelete.append(word)
            except:
                print 'url not parsed'
            
    # Use a list to delete and add words after the loop otherwise
    # the index of the previous loop will get messed up
    for word in wordsToDelete:
        sentence.remove(word)
    for word in wordsToAdd:
        sentence.append(word)
        
    return sentence

def remove_strange_symbols(sentence):
    # Remove strange symbols at the beggining and at the end of the terms
    for i in range(len(sentence)):
        sentence[i] = sentence[i].strip('.,:;&%()[]{}=+-*/\!|?~@#$\'')
        sentence[i] = sentence[i].lower()
    return sentence
    
def remove_short_words(sentence,length):
    temp_list = []
    # Remove the words with a lengh lower that length
    for i in range(len(sentence)):
        if len(sentence[i]) < length:
            temp_list.append(sentence[i])
    
    for i in range (len(temp_list)):
        sentence.remove(temp_list[i])
    return sentence
    
def remove_stopwords(sentence, stopWordList):
    # Delete all the occurences of stopWords in the sentence
    for i, stopWord in enumerate(stopWordList):
        if sentence.count(stopWord) > 0:                    
            for i in range(sentence.count(stopWord)):
                sentence.remove(stopWord)
    return sentence
    
def print_settings(stem, stopword,short,url,symbols):
    print "Using the following settings: \n"
    if(stem == "stem"):
        print "-Using the stemmed data"
    else:
        print "-Using the non-stemmed data"
    if(stopword == "remove_stopword"):
        print "-Stopwords are ignored"
    else:
        print "-Stopwords are not ignored"
    if(short == "remove_short"):
        print "-Short words ( < 3 chars ) are ignored"
    else:
        print "-Short words are not ignored"
    if(url == "stem_url"):
        print "-URLs are reduced to domain"
    else:
        print "-URLs are used as they are in the data"
    if(symbols == "remove_symbols"):
        print "-Symbols ( @$%@#!$ )are removed"
    else:
        print "-Symbols are not removed"