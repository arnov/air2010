def split(testSet):    
    # Use this parametes to decide which line are used in test
    # 0 -> line 0,4,8,12 go in test
    # 1 -> 3,7,11 etc. go in test
    # 2 -> 2,6,10 go in test
    # 3 -> 1,5,9 go in test
        
    # Open the datafile
    data = open('data_Weps3_Task2_Trial.txt','r')

    dataset = open('dataset.txt', 'w')
    # Create file to save the train set
    train = open('train.txt', 'w')
    # Create file to save the test set
    test = open('test.txt', 'w')
 
    lineno = 0
    datasetList = []
   
    for line in data:
        lineList = line.split('\t')           
        if(lineList[4].strip('\n') != 'UNKNOWN'):
            dataset.write(line)
            datasetList.append(line)
            lineno += 1 
          
    #for line in dataset:
        #if((lineno+testSet) % 4) != 0:
        #    train.write(line)		
        #else:
        #    test.write(line)	
        #lineno += 1  
    
    for i in range(len(datasetList)):
        if((i+testSet) % 4) != 0:
            train.write(datasetList[i])		
        else:
            test.write(datasetList[i])
    train.write('\n')
