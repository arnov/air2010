% AUTHORS:      Modolo Davide & Veenstra Arno
% DATE:         28 May 2010

% DESCRIPTION:  The code is used to train a classifier using the train set
% created with the python function, and then test it using the test set.
% To evaluate the classification the F-Measure is computed and a
% precision/recall curve is plotted.

% INSTRUCTIONS
% At the beginning is important to set four parameters:
%   [folder_name]:  In the python function a new dataset is created
%                   depending on which data optimization methods have been used. 
%                   At the beginning of the python code is important to
%                   write the name of the folder were the train set and the
%                   test one will be stored. The sama name has to be insert
%                   here.
%   [WEIGHTING]:    It is possible to use different types of weighting:
%                      1 -> tf (term frequency)
%                      2 -> tf-idf 
%   [CLASSIFIER]:   It is possibile to chose the type of the classifier:
%                      1 -> 1KNN (k has been setted to 1 because it gives
%                                  best result using cross-validation)
%                      2 -> LibSVM
%   [draw]:         If 1 -> the Precision/Recall curve will be drawn, 
%                   otherwise not.


%%

% PARAMETERS TO SET
folder_name = 'dataset';
WEIGHTING=1;
CLASSIFIER=2;
draw = 1;

%%
path = '../matlab_data/';
train_dataset = '/train_data_tf.csv';
train_labels = '/train_labels.csv';
test_dataset = '/test_data_tf.csv';
test_labels = '/test_labels.csv';

% 
fprintf('\n                LOADING DATA\n')
load(horzcat(path,folder_name,train_dataset))
load(horzcat(path,folder_name,train_labels))
load(horzcat(path,folder_name,test_dataset))
load(horzcat(path,folder_name,test_labels))

addpath 'Libsvm'    
addpath 'KNN'

%%


fprintf('\n                WEIGHTING\n')

if WEIGHTING==1
    % the train set and the set loaded are assigned directly to our train
    % set and test set because they are already in tf-representation
    train_data=train_data_tf;
    test_data=test_data_tf;
    clear train_data_tf;
    clear test_data_tf;


else if WEIGHTING==2
        train_data_tf = train_data;
        test_data_tf= test_data;
    
    % COMPUTE DOCUMENT FREQUENCY DF
    % (= the number of documents in the collection that contain a term t)
    %     train
    train_data_df=zeros(1,size(train_data_tf,2));
    for i=1:size(train_data_tf,2)
        train_data_df(1,i)=sum(train_data_tf(:,i)>0);
    end

    %     test
    test_data_df=zeros(1,size(test_data_tf,2));
    for i=1:size(test_data_tf,2)
        test_data_df(1,i)=sum(test_data_tf(:,i)>0);
    end

    
    % COMPUTE IDF
    %     train
    N = size(train_data_df,2);
    train_data_idf=zeros(1,size(train_data_df,2));
    for i=1:size(train_data_tf,2)
        if train_data_df(i)==0
            train_data_idf(i)=0;
        else
            train_data_idf(i)=log(N/train_data_df(i));
        end
    end


    % COMPUTE TF-IDF
    %     train
    train_data_tf_idf=zeros(size(train_data_tf,1),size(train_data_tf,2));
    for i=1:size(train_data_tf,1)
        for j=1:size(train_data_tf,2)
            train_data_tf_idf(i,j)=train_data_tf(i,j)*train_data_idf(i);
        end
    end
    
    %     test
    test_data_tf_idf=zeros(size(test_data_tf,1),size(test_data_tf,2));
    for i=1:size(test_data_tf,1)
        for j=1:size(test_data_tf,2)
            test_data_tf_idf(i,j)=test_data_tf(i,j)*train_data_idf(i);
        end
    end
    
    train_data=train_data_tf_idf;
    test_data=test_data_tf_idf;
    clear train_data_tf_idf;
    clear test_data_tf_idf;
    
    
    end % end if w2
end % end general w if

%%

if CLASSIFIER==1
    fprintf('\n                CLASSIFING 1NN')
    % CLASSIFICATION WITH KNN
    predict_labels = cvKnn(test_data', train_data', train_labels',1);
    scores = predict_labels;

    [prec,rec,fmeasure] = prec_rec(scores', test_labels, draw);
    fprintf('\nPRECISION: %f,  RECALL: %f, F-MEASURE: %f\n', prec, rec, fmeasure);

     
else if CLASSIFIER==2
    fprintf('\n                CLASSIFING LIBSVM\n')
    % CLASSIFICATION WITH LIBSVM
    cc=0.5;
    options=sprintf('-t 0 -w1 1 -w2 1 -c %f',cc);
    model=svmtrain(train_labels,train_data,options);

    [predict_labels, accuracy , scores] = svmpredict(test_labels,test_data, model); 

    scores = - scores;
    [prec,rec,fmeasure] = prec_rec(scores, test_labels, draw);
    fprintf('\nPRECISION: %f,  RECALL: %f, F-MEASURE: %f\n', prec, rec, fmeasure);
    end
end

