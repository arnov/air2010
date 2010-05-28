# AUTHORS:      Modolo Davide & Veenstra Arno
# DATE:         28 May 2010

# DESCRIPTION: This function serves as a wrapper. It first splits the original dataset into a train
# and a test set. Then it computes the csv files that are used in Matlab.

# PARAMETERS: The different feature enhancement functions can be turned on or of by adding or removing a dash after
# them, so for instance stem = "stem" will use stemming, stem = "stem-" will skip stemming. The settings are printed
# as the function begins so you can check if it's doing what is expected.


from trainSetParser import voc_train
from testSetParser import voc_test
from functions import *
from splitDataset import split

def main():
    # Use: "stem" "remove_stopword" "remove_short" "stem_url" "remove_symbols" to use everything
    # use a different string to skip somehint e.g. "stem-"
    stem = "stem"
    stopword = "remove_stopword"
    short = "remove_short"
    url = "stem_url-"
    symbols = "remove_symbols"

    print_settings(stem, stopword,short,url,symbols)
    
    # Open the datafile
    train_loc = 'data/train.txt'
    # Open the datafile
    test_loc = 'data/test.txt'

    extra_tweets = 1
    
    # Change this to save different datasets in different folders
    folder_name ='dataset'
    
    # Use 1,2,3 or 4 for different cross validation sets
    number_dataset = 1
    
    print "\nSPLITTING DATASET:",
    split(number_dataset-1)    
    print "DONE"
    
    
    # Define output files
    train_data_loc = 'matlab_data/'+folder_name+'/train_data_tf.csv'
    train_labels_loc = 'matlab_data/'+folder_name+'/train_labels.csv'
    
    test_data_loc = 'matlab_data/'+folder_name+'/test_data_tf.csv'
    test_labels_loc = 'matlab_data/'+folder_name+'/test_labels.csv'
    
    print "CREATING TRAINSET:",
    voc_train(train_loc, train_data_loc, train_labels_loc, stem, stopword, short, url, symbols, extra_tweets);    
    print "DONE"
    
    print "CREATING TESTSET:",
    voc_test(test_loc, test_data_loc, test_labels_loc, stem, stopword, short, url, symbols);    
    print "DONE"
    
if __name__ == "__main__":   
    main()
