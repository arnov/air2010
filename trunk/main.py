from trainSetParser import voc_train
from testSetParser import voc_test
from functions import *
from splitDataset import split

def main(stem, stopword,short,url,symbols):
    print_settings(stem, stopword,short,url,symbols)
    
    # Open the datafile
    train_loc = 'data/train.txt'
    # Open the datafile
    test_loc = 'data/test.txt'
    
    # Use 100 for new_data
    number_dataset = 1
    
    split(number_dataset-1)
    
    
    # Define output files
    train_data_loc = 'matlab_data/dataset_'+str(number_dataset)+'/train_data_tf.csv'
    train_labels_loc = 'matlab_data/dataset_'+str(number_dataset)+'/train_labels.csv'
    
    test_data_loc = 'matlab_data/dataset_'+str(number_dataset)+'/test_data_tf.csv'
    test_labels_loc = 'matlab_data/dataset_'+str(number_dataset)+'/test_labels.csv'
            
    voc_train(train_loc, train_data_loc, train_labels_loc, stem, stopword, short, url, symbols);
    voc_test(test_loc, test_data_loc, test_labels_loc, stem, stopword, short, url, symbols);
    
if __name__ == "__main__":   
    main("stem-","remove_stopword-","remove_short-","stem_url-","remove_symbols-")
