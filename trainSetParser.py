# AUTHORS:      Modolo Davide & Veenstra Arno
# DATE:         28 May 2010

# DESCRIPTION: the function is used to first create the vocabulary and then to represent the tweets in the 
#train set as tf (assigning the weight to be equal to the number of occurrences of term t in the tweet/document d). 

# It is initially possibile to increase the dimension of the train set adding some negative tweets that have been 
# harvested from the web. Is has been controlled in the tweetParser.py that this tweets are not containing any ambiguos 
# company name and do not refer to them. Therefor they can be used as negative example.
# Then, some text optimization methods could be applied depending on which of them have been selected in main.py
# Next, the vocabulary of the collection is going to be created
# Finally tf is compute for all the documents and the results are stored in two files (the first containing the data 
# represented as tf and the second one containing the ground truth of the set)


from functions import *
import pickle

def voc_train(train_loc, train_data_loc, train_labels_loc, stem, stopword,short, url, symbols, extra_t):   
        
    # Open the datafile
    data = open(train_loc,'a+')

    # some extra tweet could be added to the train set as negative example:
    if (extra_t == 1):
	    extra_tweets = open('data/extra_tweets.txt','r')
	    for line in extra_tweets:
        	data.write(line)
    data.seek(0)
        
        
    nrOfLines = len(data.readlines())
    # Go back to the first line
    data.seek(0)
    
    # Initialize the vocabulary as an empty list
    vocabulary = []
    #
    voc = open('voc.pickle','wb')
    # Initialize the numerical array with zeros, rows is equal to the length of the dataset
    # number of columns is equal to the lenghth of the vocabulary + some extra for labels 
    numericalArray = [[0]*1 for i in range(nrOfLines)]
    labels = []


  
    lineno = 0
   
    for line in data:
        if(lineno < nrOfLines):

            lineList = line.split('\t')       

            # Ignore empty lines
            if(len(lineList) > 2):

                # Separate the sentence by spaces and add all words to the vocabulary
                sentence = lineList[3].split()

                if(url == "stem_url"):
                    sentence = parse_url(sentence)

                if(symbols == "remove_symbols"):
                    sentence = remove_strange_symbols(sentence)

                if(short == "remove_short"):
                    sentence = remove_short_words(sentence,2)

                if(stopword == "remove_stopword"):
                    sentence = remove_stopwords(sentence)  

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
                        for i in range (len(numericalArray)):
                            numericalArray[i].append(0)
             
                
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
        
    # Save vocabulary to file
    pickle.dump(vocabulary, voc)
    voc.close()

    
    print_to_file(numericalArray,labels,train_data_loc, train_labels_loc)
