import sys 
from functions import *
import pickle



def main(stem, stopword,short,url,symbols):
    print_settings(stem, stopword,short,url,symbols)
        
    # Open the datafile
    data = open('data_Weps3_Task2_Trial.txt','r')

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

    # Variables needed for Naive Bayes
    NrOfTrue = 0.0
    NrOfFalse = 0.0
    
    NrOfWordsTrue = 0.0
    NrOfWordsFalse = 0.0
    
    # Two language models, maps a word to a count for a class
    CountInTrue = {}
    CountInFalse = {}
        

  
    lineno = 0
   
    for line in data:
        if(lineno < nrOfLines):

            lineList = line.split('\t')           

            # Separate the sentence by spaces and add all words to the vocabulary
            sentence = lineList[3].split()
            #print lineList[0]+"  "+lineList[1]+"    "+lineList[2]+"   "+lineList[3]

            # USEFUL FOR TESTS
            #for i, word in enumerate(sentence):
                #print sentence[i]

            if(url == "stem_url"):
                sentence = parse_url(sentence)

            if(symbols == "remove_symbols"):
                sentence = remove_strange_symbols(sentence)

            if(short == "remove_short"):
                sentence = remove_short_words(sentence,3)

            if(stopword == "remove_stopword"):
                sentence = remove_stopwords(sentence, stopWordList)  

            if(stem == "stem"):                
                sentence = stem_word(sentence)

            # USEFUL FOR TESTS
            #for i, word in enumerate(sentence):
                #print sentence[i]             

            # For every word add it to the vocabulary if it's not in there yet with document
            # frequency 1. If it is already in the and it's the first time in this document
            # it is encountered, add the document frequency
            for word in sentence:
                try:
                    if lineList[4].strip('\n') == 'TRUE':
                        CountInTrue[word] += 1
                    else:
                        CountInFalse[word] += 1
                    vocabulary.index(word)
                except:
                    # Don't use the word if it's going to be in the test data
                    if(lineno % 4) != 0:
                        if lineList[4].strip('\n') == 'TRUE':
                            CountInTrue[word] = 1
                        else:
                            CountInFalse[word] = 1
                        vocabulary.append(word)                  
         
            
            #Fill the numerical array with values
            for word in sentence:
                try:
                    numericalArray[lineno][vocabulary.index(word)] = sentence.count(word)
                except:
                    continue

            if lineList[4].strip('\n') == 'TRUE':
                #numericalArray[lineno][0] = 1
                labels.append(1)
                # Update naive bayes statistics for train set only
                if(lineno % 4) != 0:
                    NrOfWordsTrue += len(sentence)
                    NrOfTrue += 1
            else:
                #numericalArray[lineno][0] = 0
                labels.append(-1)
                NrOfFalse += 1
                if(lineno % 4) != 0:
                    NrOfWordsFalse += len(sentence)
                    NrOfFalse += 1    
            
            lineno += 1   

    print "\nVocabulary length: "
    print len(vocabulary)
    
    print "\np(T) = "
    print NrOfTrue/(NrOfTrue+NrOfFalse)
    
    print "\np(comput|True) = "
    print CountInTrue['comput']/NrOfWordsTrue
    
    for i in range (len(numericalArray)):
        del numericalArray[i][len(vocabulary):14632]
        
    # Save vocabulary to file
    pickle.dump(vocabulary, voc)
    voc.close()

    
    #print_to_file(numericalArray,labels)
    print "\nThe matlab_data files are not updated!\n"

    # Calculate probabilities for test example
    data.seek(0)
    lineno = 0
    nrOfTest = 0
    NrOfErrors = 0.0
    for line in data:
        if(lineno < nrOfLines and (lineno % 4) == 0):
            lineList = line.split('\t')                       
            sentence = lineList[3].split()
            
            pTrue = 1.0
            pFalse = 1.0
            
            for word in sentence:
                # Ugly hack, need smoothing, if the word is never seen just multiply by 1
                try:                    
                    pTrue *= CountInTrue[word]/NrOfWordsTrue
                    pFalse *= CountInFalse[word]/NrOfWordsFalse
                except:
                    pTrue *= 1
                    pFalse *= 1
            
            pTrue *= NrOfTrue/(NrOfTrue+NrOfFalse)
            pFalse *= NrOfFalse/(NrOfTrue+NrOfFalse)
            
                        
            if(pTrue > pFalse):
                if(lineList[4].strip('\n') != 'TRUE'):
                    print NrOfErrors
                    print "ERROR PREDICTED TRUE"
                    print line
            else:
                if(lineList[4].strip('\n') != 'FALSE'):
                    NrOfErrors += 1
                    print "ERROR PREDICTED FALSE"
                    print line
            nrOfTest += 1
        lineno += 1
    
    print NrOfErrors
    print "-"
    print nrOfTest  
    print "Accuracy"
    print 1-NrOfErrors/nrOfTest

if __name__ == "__main__":   
    try:
        main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    except:
        main("stem","remove_stopword","remove_short","stem_url","remove_symbols" )
