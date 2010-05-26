from functions import *
import pickle

""" Opens a file with test tweets and outputs a CSV file that can be used as testset in Matlab """

def voc_test(test_loc, test_data_loc, test_labels_loc, stem, stopword,short, url, symbols):

        
    # Open the datafile
    data = open(test_loc, 'r')    

    # Define output files
    test_data = open(test_data_loc, 'w')
    test_labels = open(test_labels_loc, 'w')

    nrOfLines = len(data.readlines())
    # Go back to the first line
    data.seek(0)    
  
    # Read the vocabulary from file
    voc = open('voc.pickle','rb')
    vocabulary = pickle.load(voc)
    voc.close()
    
    # Initialize the numerical array with zeros, rows is equal to the length of the dataset
    # number of columns is equal to the lenghth of the vocabulary + some extra for labels 
    numericalArray = [[0]*(len(vocabulary)+1) for i in range(nrOfLines)]
    labels = []

 
    lineno = 0
   
    for line in data:
        if(lineno < nrOfLines):

            lineList = line.split('\t')
            

            # Separate the sentence by spaces
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

        
    # Print it to file
    for i in range(len(numericalArray)):
        test_data.write(str(numericalArray[i]).strip('[]'))
        test_data.write('\n')
        test_labels.write(str(labels[i]).strip('[]'))
        test_labels.write('\n')

