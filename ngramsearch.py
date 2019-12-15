import jieba
from tsim import TopSim
from tqdm import tqdm

class ngram_search(object):
    
    def __init__(self,data,kb,ngram = 4,similarity = 0.6,k=1,e=0.7,simFunc="tversky"): 
        self.n = ngram
        self.similarity = similarity
        self.data = data
        self.kb = kb
        self.k = k
        self.e = e
        self.simFunc = simFunc
        self.cut_data,self.offset = self.cut_words()
        self.ts = TopSim(self.kb)
        self.candidates = self.get_candidates()
        self.cand_name,self.cand_off,self.cand_with_off = self.get_candidates_name()
        
    def cut_words(self):
        print('starting build ngram list')
        print('ngram',self.n)
        result = []
        offset = []
        for d in tqdm(self.data):
#             print(d)
#             print(' '.join(jieba.cut(d)))
            tmp = list(jieba.cut(d))
            n = len(tmp)
            tmp_off = []
            tmp_off.append((0,len(tmp[0])))
#             tmp_off = [len(''.join(tmp[:i])) for i in range(len(tmp))]
            for i in range(1,len(tmp)):
                tmp_off.append((tmp_off[-1][1],tmp_off[-1][1]+len(tmp[i])))
            for j in range(2,self.n+1):
                for i in range(j-1,n):
                    tmp.append(''.join(tmp[i-j+1:i+1]))
                    tmp_off.append((tmp_off[i-j+1][0],tmp_off[i][1]))
#                     tmp_off.append(''.join(tmp[:i-n+1]))
            result.append(tmp)
            offset.append(tmp_off)
#         print(result[0])
#         print(offset[0])
        return result,offset
    
    def get_candidates(self):
#         self.similarity = similarity
        print('starting build candidates list')
        print('similarity:',self.similarity)
        candidates = []
        for dt in tqdm(self.cut_data):
            ts_result = []
            for i in dt:
                tmp = self.ts.search(i,k = self.k,e = self.e,worstSim = self.similarity,simFunc=self.simFunc)
                if tmp:
#                 if tmp and tmp[0][0] > self.similarity:
                    ts_result.append(tmp)
                else:
                    ts_result.append([])
            candidates.append(ts_result)
        return candidates
                                                     
    def get_candidates_name(self):
        print('starting get candidates name and offset')
        cand_name = []
        cand_offset = []
        cand_with_off = []
        cand_with_offend = []
        for i in tqdm(range(len(self.candidates))):
            cand = []
            off = []
            c_o_s = {}
            c_o_e = {}
            for j in range(len(self.candidates[i])):    
                if self.candidates[i][j]:
#                     print(self.candidates[i][j])
#                     print(self.candidates[i][j][0][1][0])
#                     print(self.kb[self.candidates[i][j][0][1][0]])
                    token = self.kb[self.candidates[i][j][0][1][0]]
                    token_off = self.offset[i][j]
#                     print(token_off)
                    begin = str(token_off[0])
                    end = str(token_off[1]) 
#                     if str(token_off[0]+1) in c_o:
#                         if token == c_o[str(token_off[0]+1)][-1][1]:
#                             continue
#                     if key_value not in c_o:
                    if end in c_o_e:
                        if token in c_o_e[end]:
                            continue
                    else:
                        c_o_e[end] = set()
                    if begin in c_o:
                        if token == c_o_s[begin][-1][1]:
                            continue
                    else:
                        c_o_s[begin] = []
                    cand.append(token)
                    off.append(token_off)
                    c_o_s[begin].append((token_off[1],token))
                    c_o_e[end].add(token)
            cand_name.append(cand)
            cand_offset.append(off)
            cand_with_off.append(c_o_s)
            cand_with_offend.append(c_o_e)
#         print(cand_with_offend[0])
        return cand_name,cand_offset,cand_with_off