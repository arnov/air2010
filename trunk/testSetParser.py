from functions import *
import sys 
import pickle

""" Opens a file with test tweets and outputs a CSV file that can be used as testset in Matlab """

def main():

        
    # Open the datafile
    data = open('extra_tweets.txt', 'r')    

    # Define output files
    test_data = open('../matlab_data/test_data_tf.csv', 'w')
    test_labels = open('../matlab_data/test_labels.csv', 'w')

    nrOfLines = len(data.readlines())
    # Go back to the first line
    data.seek(0)
    
    # Prototype of the stopword list
    stopWordList =["the","and","was","were","will","also","for","all","with","other","que","has","con","sin","soy","estoy","ser",""]
    
    # Read the vocabulary from file
    voc = open('voc.pickle','rb')
    vocabulary = pickle.load(voc)
    voc.close()
    
    # Initialize the numerical array with zeros, rows is equal to the length of the dataset
    # number of columns is equal to the lenghth of the vocabulary + some extra for labels 
    numericalArray = [[0]*14632 for i in range(nrOfLines)]
    labels = []


  
    lineno = 0
   
    for line in data:
        if(lineno < nrOfLines):

            lineList = line.split('\t')           

            # Separate the sentence by spaces
            sentence = lineList[3].split()

            sentence = parse_url(sentence)
            
            sentence = remove_strange_symbols(sentence)
            
            sentence = remove_short_words(sentence,3)
            
            sentence = remove_stopwords(sentence, stopWordList)                   
              
            
            #Fill the numerical array with values
            for word in sentence:
                try:
                    numericalArray[lineno][vocabulary.index(word)] = sentence.count(word)
                except:
                    continue

            if lineList[4].strip('\n') == 'TRUE':
                #numericalArray[lineno][0] = 1
                labels.append(1)
            else:
                #numericalArray[lineno][0] = 0
                labels.append(-1)
                
            lineno += 1   

    print "\nVocabulary length: "
    print len(vocabulary)
    print vocabulary[17]
    
    for i in range (len(numericalArray)):
        del numericalArray[i][len(vocabulary):14632]
        
    # Print it to file
    for i in range(len(numericalArray)):
        test_data.write(str(numericalArray[i]).strip('[]'))
        test_data.write('\n')
        test_labels.write(str(labels[i]).strip('[]'))
        test_labels.write('\n')

        
if __name__ == "__main__":    
    main()
