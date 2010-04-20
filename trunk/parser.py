def main():
    # Open the datafile
    data = open('../data/data_Weps3_Task2_Trial.txt', 'r')
    # Create file to save the output
    train_data = open('../matlab_data        rain_data_tf.csv', 'w')
    test_data = open('../matlab_data        est_data_tf.csv', 'w')
    #train_labels = open('../matlab_data/train_labels.csv', 'w')
    #test_labels = open('../matlab_data/test_labels.csv', 'w')
    
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
    numericalArray = [[0]*10632 for i in range(2297)]
    labels = [[0]*2297]


  
    lineno = 0
    for line in data:
        if lineno < 2:

            temp_list = []

            lineList = line.split('\t')

            # Separate the sentence by spaces and add all words to the vocabulary
            sentence = lineList[3].split()        
            print lineList[0]+"  "+lineList[1]+"    "+lineList[2]+"   "+lineList[3]

            # Remove strange symbols at the beggining and at the end of the terms
            for i in range(len(sentence)):
                sentence[i] = sentence[i].strip('.,:;&%()[]{}=+-*/\!|?~@#$\'')
                sentence[i] = sentence[i].lower()

            # Remove the words with a lengh lower that 3
            for i in range(len(sentence)):
                if len(sentence[i]) < 3:
                    temp_list.append(sentence[i])

            for i in range (len(temp_list)):
                sentence.remove(temp_list[i])

            # USEFUL FOR TESTS
            for i, word in enumerate(sentence):
                print sentence 
        
            # Delete all the occurences of stopWords in the sentence
            for i, stopWord in enumerate(stopWordList):
                if sentence.count(stopWord) > 0:                    
                    for i in range(sentence.count(stopWord)):
                        sentence.remove(stopWord)

        # USEFUL FOR TESTS
            for i, word in enumerate(sentence):
                print sentence 



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


    print len(vocabulary)
    print len(wordOrderList)
    
    # Print all the numerical data to the file (Beware file gets about 100 MB!)
    for i in range(len(numericalArray)):
  
                if (i % 4) == 0:
                        test_data.write(str(numericalArray[i]).strip('[]'))
                        test_data.write('\n')
                        #test_labels.write(str(labels[i]).strip('[]'))
                        #test_labels.write('\n')
                else:
                        train_data.write(str(numericalArray[i]).strip('[]'))
                        train_data.write('\n')
                        #train_labels.write(str(labels[i]).strip('[]'))
                        #train_labels.write('\n')

                
        #labelsMatlab.write(labels[lineno])
        #dataMatlab.write('\n')
        
if __name__ == "__main__":    
    main()
