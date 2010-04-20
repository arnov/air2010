def print_to_file(numericalArray):
    # Create file to save the output
    train_data = open('../matlab_data/train_data_tf.csv', 'w')    
    #train_labels = open('../matlab_data/train_labels.csv', 'w')
    test_data = open('../matlab_data/test_data_tf.csv', 'w')
    #test_labels = open('../matlab_data/test_labels.csv', 'w')
    
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

def parse_url(sentence):
    wordsToAdd = []
    wordsToDelete = []
    for word in sentence:
        if word[0:4] == 'http':
            urlInfo = word.split('/')
            wordsToDelete.append(word)
            try:
                wordsToAdd.append(urlInfo[2].strip('www.').split('.')[0])
            except:
                continue

    # Use a list to delete and add words after the loop otherwise
    # the index of the previous loop will get messed up
    for word in wordsToDelete:
        sentence.remove(word)
    for word in wordsToAdd:
        sentence.append(word)
        
    return sentence
