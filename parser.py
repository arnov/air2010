from functions import *
import sys 

""" To use all stemming and word reducing function call as:
 python parser.py "stem" "remove_stopword" "remove_short" "stem_url" "remove_symbols"
 To skip a function just use a different string e.g.:
 python parser.py "-" "remove_stopword" "remove_short" "stem_url" "remove_symbols"
 will use the non stemmed data, but does call the other function, remove_stopword etc. """

def main(stem, stopword,short,url,symbols):
    print_settings(stem, stopword,short,url,symbols)
        
    # Open the datafile
    if(stem == "stem"):
        data = open('stemmed_data.txt', 'r')    
    else:
        data = open('../data/data_Weps3_Task2_Trial.txt','r')
    
    # Prototype of the stopword list
    stopWordList =["the","and","was","were","will","also","for","all","with","other","que","has","con","sin","soy","estoy","ser",""]
    
    # Initialize the vocabulary as an empty dictionary it maps between words and the number of
    # documents they occur in.
    vocabulary = {}
    # The wordOrderList is used to get the correct index for when we need to add a value to
    # the numericalArray
    wordOrderList = []
    # Initialize the numerical array with zeros, rows is equal to the length of the dataset
    # number of columns is equal to the lenghth of the vocabulary + some extra for labels 
    numericalArray = [[0]*14632 for i in range(2297)]
    labels = []


  
    lineno = 0
    for line in data:
        if lineno < 2297:

            lineList = line.split('\t')
                        
            # Separate the sentence by spaces and add all words to the vocabulary
            sentence = lineList[3].split()
            #print lineList[0]+"  "+lineList[1]+"    "+lineList[2]+"   "+lineList[3]

            # USEFUL FOR TESTS
            #for i, word in enumerate(sentence):
                #print sentence[i]

            if(url == "stem_url"):
                sentence = parse_url(sentence)

            if(symbols == "remove_symbols")    :
                sentence = remove_strange_symbols(sentence)

            if(short == "remove_short"):
                sentence = remove_short_words(sentence,3)

            if(stopword == "remove_stopword"):
                sentence = remove_stopwords(sentence, stopWordList)       

            # USEFUL FOR TESTS
            #for i, word in enumerate(sentence):
                #print sentence[i] 



            # For every word add it to the vocabulary if it's not in there yet with document
            # frequency 1. If it is already in the and it's the first time in this document
            # it is encountered, add the document frequency
            for word in sentence:
                try:
                    vocabulary[word] += 1  
                    wordOrderList.index(word)
                except:
                    vocabulary[word] = 1
                    wordOrderList.append(word)
         
            
            #Fill the numerical array with values
            for word in sentence:
                numericalArray[lineno][wordOrderList.index(word)] = sentence.count(word)

            if lineList[4].strip('\n') == 'TRUE':
                #numericalArray[lineno][0] = 1
                labels.append(1)
            else:
                #numericalArray[lineno][0] = 0
                labels.append(-1)
                
        lineno += 1   

    print "\nVocabulary length: "
    print len(vocabulary)
    print len(wordOrderList)
    
    #print_to_file(numericalArray,labels)
        
if __name__ == "__main__":    
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
