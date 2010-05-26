% % Run python script in windows
% [s,Python_output] = dos('C:\Python26\python.exe parser.py "stem" "remove_stopword" "remove_short" "stem_url" "remove_symbols"')
% %%
% % Run python script in linux
% system(sprintf('python parser.py "stem" "remove_stopword" "remove_short" "stem_url" "remove_symbols"'))
% 
% %% WINDOWS
% addpath ..\code\Libsvm\
% addpath ..\code\KNN\
% addpath ..\code

%% LINUX
addpath 'Libsvm'    
addpath 'KNN'
% addpath 'code'
%%
fprintf('\n                LOADING DATA\n')

load('../matlab_data/dataset_O1/train_data_tf.csv')
load('../matlab_data/dataset_O1/test_data_tf.csv')
load('../matlab_data/dataset_O1/train_labels.csv')
load('../matlab_data/dataset_O1/test_labels.csv')


%%
% Here we can select with type of weighting we want use:
% 1 = tf
% 2 = tf-idf
WEIGHTING=1;
% Here we can select with type of classifier we want use:
% 1 = knn
% 2 = svn
CLASSIFIER=2;


fprintf('\n                WEIGHTING\n')

if WEIGHTING==1
    train_data=train_data_tf;
    test_data=test_data_tf;


else if WEIGHTING==2
    
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
    
    
    end % end if w2
end % end general w if

%%

fprintf('\n                CLASSIFING\n')
% CLASSIFIER = 1;
% clear scores;
% clear predict_label

if CLASSIFIER==1
    % CLASSIFICATION WITH KNN
    predict_labels = cvKnn(test_data', train_data', train_labels',2);
    scores = predict_labels;

else if CLASSIFIER==2
    
    % CLASSIFICATION WITH LIBSVM
    cc=0.5;
    options=sprintf('-t 0 -w1 1 -w2 1 -c %f',cc);
    model=svmtrain(train_labels,train_data,options);

    [predict_label, accuracy , scores] = svmpredict(test_labels,test_data, model); 
    end
end

% Compute the percentage of correct positive and correct negative
% classified
pos=sum(predict_label(test_labels==1)==1)/sum(test_labels==1); 
neg=sum(predict_label(test_labels==-1)==-1)/sum(test_labels==-1);

%
scores = - scores;

[prec,rec,fmeasure] = prec_rec(scores, test_labels, 1);

fprintf('\nPOS: %f, fNEG: %f, PRECISION: %f,  RECALL: %f, F-MEASURE: %f\n', pos, neg, prec, rec, fmeasure);


%% 


% r = 1;
% t = 1;
% 
% for i=1:size(train_data_tf,1)
%     if mod(i,4)==0
%             test(t,:) = train_data_tf(i,:);
%             test_label(t,:) = train_labels(i,:);
%             t = t+1;
%             fprinf('Row: %f',i);
%     else
%             train(r,:) = train_data_tf(i,:);
%             train_label(r,:) = train_labels(i,:);
%             r = r+1;
%     end
% end

% for i=1:size(output,1)
%         if output(i)<0
%             output2(i)=-1;
%         else
%             output2(i)=1;
%         end
% end
% output2 = output2';
% pos=sum(output2(gt==1)==1)/sum(gt==1) 
% neg=sum(output2(gt==-1)==-1)/sum(gt==-1)
% [rec,prec,ap] = prec_rec(output, gt, 1);
% 
% 
% train = horzcat(train_data, train_labels);
% test = horzcat(test_data, test_labels);
% for i=1:size(train,1)
%         if train(i,size(train,2))==-1
%             train(i,size(train,2))=2;
%         end
% end
% 
% for i=1:size(test,1)
%         if test(i,size(test,2))==-1
%             test(i,size(test,2))=2;
%         end
% end
% 
% [predict, accuracy] = Naive_Bayes(train, test)

% [AA,BB]=sort(dec_values, 'descend');
% gt=test_labels(BB);
% score=AA;
% prec_rec(dec_values, test_labels);
%[prec, tpr, fpr, thresh] = prec_rec(dec_values, test_labels, 'plotPR', 1);

% RESULTS with stemmed data (beforehand), stemmed url, del short words, del
% symbols # nr of terms in the voc: 8741
% TF
% Accuracy = 85.3913% (491/575) (classification)
% pos = 0.7939
% neg = 0.8934

% TF-IDF 
% Accuracy = 68.1739% (392/575) (classification)
% pos = 0.7895
% neg = 0.6110

% RESULTS:
% # of terms in the voc: 14374

% TF
% Accuracy = 64.5217% (371/575) (classification)
% pos =    0.4815
% neg =    0.7651

% TF-IDF
% Accuracy = 57.2174% (329/575) (classification)
% pos =    0.6955
% neg =    0.4819

% _________________________________________________

% RESULTS after the elimination of the different symbols at the beggining
% and at the and of all the words.  Symbols: ".,:;&%()[]{}=!|?*~@#$\'"
% # of terms in the voc: 12520

% TF
% Accuracy = 65.3913% (376/575) (classification)
% pos =    0.5309
% neg =    0.7440

% TF-IDF
% Accuracy = 57.7391% (332/575) (classification)
% pos =    0.6420
% neg =    0.5301

% ___________________________________________________

% RESULTS after having setted all the words in lower case
% # of terms in the voc: 11013

% TF
% Accuracy = 66.9565% (385/575) (classification)
% pos =    0.5309
% neg =    0.7711

% TF-IDF
% Accuracy = 61.0435% (351/575) (classification)
% pos =    0.6667
% neg =    0.5693

% ___________________________________________________

% RESULTS after having deleted the words with lengh < 3 
% # of terms in the voc: 10632

% TF
% Accuracy = 65.5652% (377/575) (classification)
% pos =    0.5185
% neg =    0.7560

% TF-IDF
% Accuracy = 62.087% (357/575) (classification)
% pos =    0.7037
% neg =    0.5602

