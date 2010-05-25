from functions import *
import pickle


""" To use all stemming and word reducing function call as:
 python parser.py or, pass all settings explicitely:
 python parser.py "stem" "remove_stopword" "remove_short" "stem_url" "remove_symbols"
 To skip a function just use a different string e.g.:
 python parser.py "-" "remove_stopword" "remove_short" "stem_url" "remove_symbols"
 will use the non stemmed data, but does call the other function, remove_stopword etc. """

def voc_train(train_loc, train_data_loc, train_labels_loc, stem, stopword,short, url, symbols):   
        
    # Open the datafile
    data = open(train_loc,'a+')
    extra_tweets = open('extra_tweets.txt','r')
    
    for line in extra_tweets:
        data.write(line)
    data.seek(0)
        
        
    nrOfLines = len(data.readlines())
    # Go back to the first line
    data.seek(0)
    
    # Prototype of the stopword list
    stopWordList =["the","and","was","were","will","also","for","all","with","other","que","has","con","sin","soy","estoy","ser",""]
    
    # Initialize the vocabulary as an empty list
    vocabulary = []
    #
    voc = open('voc.pickle','wb')
    # Initialize the numerical array with zeros, rows is equal to the length of the dataset
    # number of columns is equal to the lenghth of the vocabulary + some extra for labels 
    numericalArray = [[0]*14632 for i in range(nrOfLines)]
    labels = []


  
    lineno = 0
   
    for line in data:
        if(lineno < nrOfLines):

            lineList = line.split('\t')           

            # Separate the sentence by spaces and add all words to the vocabulary
            sentence = lineList[3].split()

            if(url == "stem_url"):
                sentence = parse_url(sentence)

            if(symbols == "remove_symbols"):
                sentence = remove_strange_symbols(sentence)

            if(short == "remove_short"):
                sentence = remove_short_words(sentence,2)

            if(stopword == "remove_stopword"):
                sentence = remove_stopwords(sentence, stopWordList)  

            if(stem == "stem"):                
                sentence = stem_word(sentence)                         

            # For every word add it to the vocabulary if it's not in there yet with document
            # frequency 1. If it is already in the and it's the first time in this document
            # it is encountered, add the document frequency
            for word in sentence:
                try:
                    vocabulary.index(word)
                except:
                    vocabulary.append(word)                  
         
            
            #Fill the numerical array with values
            for word in sentence:
                try:
                    numericalArray[lineno][vocabulary.index(word)] = sentence.count(word)
                except:
                    continue

            if lineList[4].strip('\n') == 'TRUE':
                labels.append(1)
            else:
                labels.append(-1)
                
            lineno += 1

    print "\nVocabulary length: "
    print len(vocabulary)
    
    for i in range (len(numericalArray)):
        del numericalArray[i][len(vocabulary):14632]
        
    # Save vocabulary to file
    pickle.dump(vocabulary, voc)
    voc.close()

    
    print_to_file(numericalArray,labels,train_data_loc, train_labels_loc)
