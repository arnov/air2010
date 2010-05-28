# AUTHORS:      Modolo Davide & Veenstra Arno
# DATE:         28 May 2010

# DESCRIPTION: As the test dataset has not been released yet,
# the train dataset is going to be splitted in two parts: train and test sets. 

# The function accepts one parameter as input:
# [testSet]:    This paramenter can take the following values: 
# 	 	0, 1, 2, 3 and 99 (if a 4 is insert it will work as a 0, a 5 as a 1, and so on...)
# 		Values 0, 1, 2 and 3 split the trial train set: "data_Weps3_Task2_Trial.txt" file 
#		in four differnt train and test sets
#		Value 99 split the new train set: "weps-3_task-2_training.tsv" released few days ago in train and test set. 


def split(testSet):    
    # Use this parametes to decide which line are used in test
    # 0 -> line 0,4,8,12 go in test
    # 1 -> 3,7,11 etc. go in test
    # 2 -> 2,6,10 go in test
    # 3 -> 1,5,9 go in test
        
    # Open the datafile
    if(testSet != 99):
        data = open('data/data_Weps3_Task2_Trial.txt','r')
        splitFactor = 4
    else:
        data = open('data/weps-3_task-2_training.tsv','r')
        splitFactor = 10

    tempset = open('data/dataset.txt', 'w')
    # Create file to save the train set
    train = open('data/train.txt', 'w')
    # Create file to save the test set
    test = open('data/test.txt', 'w')
 
    lineno = 0
    datasetList = []
   
    # Skip all examples labelled 'UNKNOWN'
    for line in data:
        lineList = line.split('\t')           
        if(lineList[4].strip('\n') != 'UNKNOWN'):
            tempset.write(line)
            datasetList.append(line)
            lineno += 1 

    
    for i in range(len(datasetList)):
        if((i+testSet) % splitFactor) != 0:
            train.write(datasetList[i])         
        else:
            test.write(datasetList[i])
    
if __name__ == "__main__":  
    split(0)
