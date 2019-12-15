from extratools.mathtools import safediv
from tqdm import tqdm
import numpy as np

def evaluate_cand_off(cand_with_off,ground_truth,ment_data,k=0.6):
    recall = []
    precision = []
    f1 = []
    under_k = []
    error = []
    error_off = []
    
    for i in tqdm(range(len(ground_truth))):
        tp = 0
        for j in ground_truth[i]:
            if j[0] in cand_with_off[i]:
                if j[1] in cand_with_off[i][j[0]][0]:
                    tp += 1
            else:
                if j[1] in ment_data[i]:
                    error_off.append(i)        
        r = tp/len(ground_truth[i])
        if r < k:
            under_k.append(i)
        p = tp/len(cand_with_off[i].keys())
        f = safediv(2*r*p,r+p)
        
        recall.append(r)
        precision.append(p)
        if  f > 1 or np.isnan(f):
            error.append(i)
            f1.append(0)
        else:
            f1.append(f)
            
    av_recl = sum(recall)/len(recall)
    av_pre = sum(precision)/len(precision)
    av_f1 = sum(f1)/len(f1)
    
    print('average recall: {}'.format(av_recl))
    print('average precision: {}'.format(av_pre))
    print('average f1: {}'.format(av_f1))
    print('error number: {}'.format(len(error)))
    print('total number: {}'.format(len(ment_data)))
    print('error rate: {}'.format(len(error)/len(ment_data)))
    print('error off: {}'.format(len(error_off)))
    print('recall under{} : {}'.format(k,len(under_k)))
    return recall, precision,f1,error,error_off,under_k