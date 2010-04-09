def main():
    # Open the datafile
    data = open('../weps-3/data/task-2/trial/data_Weps3_Task2_Trial.txt', 'r')
    # Creat a file to save the output
    dataMatlab = open('../code/dataMatlab.csv', 'w')
    
    # Prototype of the stopword list
    stopWordList = ['I',"the","it"]
    
    # Initialize the vocabulary as an empty dictionary it maps between words and the number of
    # documents they occur in.
    vocabulary = {}
    # The wordOrderList is used to get the correct index for when we need to add a value to
    # the numericalArray
    wordOrderList = []
    # Initialize the numerical array with zeros, rows is equal to the length of the dataset
    # number of columns is equal to the lenghth of the vocabulary + some extra for labels 
    numericalArray = listoflists=[[0]*14410 for i in range(2297)]

    
    lineno = 0
    for line in data:
        if lineno < 2297:
            
            lineList = line.split('\t')
            # Separate the sentence by spaces and add all words to the vocabulary
            sentence = lineList[3].split()        
            

            # Delete all the occurences of stopWords in the sentence
            for i, stopWord in enumerate(stopWordList):
                if sentence.count(stopWord) > 0:                    
                    for i in range(sentence.count(stopWord)):
                        sentence.remove(stopWord)
            
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
            
            # Correct for words that appear multiple times in one document.
            for word in sentence:
                if sentence.count(word) != 1: 
                    vocabulary[word] -= float(((sentence.count(word)-1))/float(sentence.count(word)))
     
            
            #Fill the numerical array with values
            for word in sentence:
                numericalArray[lineno][wordOrderList.index(word)+1] = sentence.count(word)
            # add the label, 1 if it's a positive example, 0 otherwise
            if lineList[4].strip('\n') == 'TRUE':
                numericalArray[lineno][0] = 1
            else:
                numericalArray[lineno][0] = 0
                
        lineno += 1   


    print len(vocabulary)
    print len(wordOrderList)
    
    # Print all the numerical data to the file (Beware file gets about 100 MB!)
    for i in range(len(numericalArray)):
        dataMatlab.write(str(numericalArray[i]).strip('[)').strip(']'))
        dataMatlab.write('\n')

        
if __name__ == "__main__":    
    main()
