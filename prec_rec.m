function [rec,prec,ap] = prec_rec(dec_values, gt, draw)

% compute precision/recall
[AA,BB]=sort(dec_values, 'descend');
tp=gt(BB)>0;
fp=gt(BB)<0;

fp=cumsum(fp);
tp=cumsum(tp);
rec=tp/sum(gt>0);
prec=tp./(fp+tp);

% compute average precision
ap=0;
for t=0:0.1:1
    p=max(prec(rec>=t));
    if isempty(p)
        p=0;
    end
    ap=ap+p/11;
end

if draw
    % plot precision/recall
    plot(rec,prec,'-');
    grid;
    xlabel 'recall'
    ylabel 'precision'
    title(sprintf('AP = %.3f',1, ap));
end
