import sys 
from functions import *
import pickle



def main(stem, stopword,short,url,symbols):
    print_settings(stem, stopword,short,url,symbols)
        
    # Open the datafiles
    train = open('train.txt','r')
    test = open('test.txt','r')

    nrOfLines = len(train.readlines())
    # Go back to the first line
    train.seek(0)
    
    # Prototype of the stopword list
    stopWordList =["the","and","was","were","will","also","for","all","with","other","que","has","con","sin","soy","estoy","ser",""]
    

    # Variables needed for Naive Bayes
    NrOfTrue = 0.0
    NrOfFalse = 0.0
    
    NrOfWordsTrue = 0.0
    NrOfWordsFalse = 0.0
    
    # Two language models, maps a word to a count for a class
    CountInTrue = {}
    CountInFalse = {}
        

  
    lineno = 0
   
    for line in train:
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

             

            # For every word if it's in a positive example add it
            # to the CountInTrue dict if it's false add it to the
            # CountInFalse, if it's not yet seen create it in the dict
            for word in sentence:
                try:
                    if lineList[4].strip('\n') == 'TRUE':
                        CountInTrue[word] += 1
                    else:
                        CountInFalse[word] += 1
                except:
                    if lineList[4].strip('\n') == 'TRUE':
                        CountInTrue[word] = 1
                    else:
                        CountInFalse[word] = 1
          
         
            


            if lineList[4].strip('\n') == 'TRUE':
                NrOfWordsTrue += len(sentence)
                NrOfTrue += 1
            else:
                NrOfFalse += 1
                NrOfWordsFalse += len(sentence)
                NrOfFalse += 1    
            
            lineno += 1   
    


    # Calculate probabilities for test example
    lineno = 0
    NrOfTest = 0
    NrOfErrors = 0.0
    
    FalsePos = 0.0
    FalseNeg = 0.0
    TruePos = 0.0
    TrueNeg = 0.0

    
    for line in test:        
        lineList = line.split('\t')                       
        sentence = lineList[3].split()
        
        pTrue = 1.0
        pFalse = 1.0
        
        for word in sentence:
            # If the word exist in both dictionary just use the counts
            if word in CountInTrue and word in CountInFalse:
                pTrue *= CountInTrue[word]/NrOfWordsTrue
                pFalse *= CountInFalse[word]/NrOfWordsFalse
            # If it appears in only one make it more likely that it belongs
            # to that class
            elif word in CountInTrue:
                pTrue *= 1.0
                pFalse *= 0.7
            elif word in CountInFalse:
                pTrue *= 0.7
                pFalse *= 1.0
            # If it doesn't belong to any just ignore it    
            else:
                pTrue *= 1.0
                pFalse *= 1.0

        pTrue *= NrOfTrue/(NrOfTrue+NrOfFalse)
        pFalse *= NrOfFalse/(NrOfTrue+NrOfFalse)

        #print pTrue - pFalse
        
        
        if(pTrue > pFalse):
            #print "l"
            if(lineList[4].strip('\n') != 'TRUE'):
                NrOfErrors += 1
                FalsePos += 1
                #print "ERROR PREDICTED TRUE"
                #print line
            else:
                TruePos += 1
        else:
            #print "-1"
            if(lineList[4].strip('\n') != 'FALSE'):
                NrOfErrors += 1
                FalseNeg += 1
                #print "ERROR PREDICTED FALSE"
                #print line
            else:
                TrueNeg += 1
        NrOfTest += 1
        lineno += 1
        #print "-->"
        
    print NrOfErrors
    print "-"
    print NrOfTest  
    print "\nAccuracy"
    print 1-NrOfErrors/NrOfTest
    print "\nRecall"
    print TruePos/(TruePos+FalseNeg)
    print "\nPrecision"
    print TruePos/(TruePos+FalsePos)
    print "\nConf Matrix"
    print str(TruePos/(TruePos+FalsePos)) + " " + str(FalsePos/(TruePos+FalsePos))
    print str(FalseNeg/(FalseNeg+TrueNeg)) + " " + str(TrueNeg/(FalseNeg+TrueNeg))

if __name__ == "__main__":   
    try:
        main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    except:
        main("stem","remove_stopword","remove_short","stem_url","remove_symbols" )
