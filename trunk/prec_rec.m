% AUTHORS:      Modolo Davide & Veenstra Arno
% DATE:         28 May 2010

% DESCRIPTION:  The function is used to compute precision, recall, F-Measure
%               and to draw a precision/recall curve

% INPUT DATA:   [scores]: It is a vector containing a score for every
%                         example in the test set
%               [gt]:     It is a vector with the groud truth of the test set
%               [draw]:   If draw = 1 the P/R curve is going to be drawn,
%                         not otherwise

function [precision,recall,Fmeasure] = prec_rec(scores, gt, draw)


% compute balanced F measure with alpha=0.5
predict_labels = zeros(size(scores,1),1);
for i=1:size(scores,1)
    if scores(i) > 0
        predict_labels(i)=1;
    else
        predict_labels(i)=-1;
    end
end
        
true_positive = sum(predict_labels(gt==1)==1);
precision = true_positive/sum(predict_labels==1);
recall = true_positive/sum(gt>0);

Fmeasure = 2*precision*recall/(precision+recall);


% compute precision/recall
[AA,BB]=sort(scores, 'descend');
tp=gt(BB)>0;
fp=gt(BB)<0;

fp=cumsum(fp);
tp=cumsum(tp);
rec=tp/sum(gt>0);
prec=tp./(fp+tp);

% draw precision/recall curve
if draw
    % plot precision/recall
    plot(rec,prec,'-');
    grid;
    xlabel 'recall'
    ylabel 'precision'
    title(sprintf('F-measure = %f', Fmeasure));
end
