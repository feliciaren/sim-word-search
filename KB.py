import json
from tqdm import tqdm
import os
from random import choice
from itertools import groupby
import numpy as np 

class KB(object):
    def __init__(self,kb_directory):
        print("start loading kb_data...")
        self.kb_directory = kb_directory
        self.id2kb,self.types,self.predicate = self.get_id2kb()
        self.kb2id = self.get_kb2id()
        self.kb = list(self.kb2id.keys())
        self.id = list(self.id2kb.keys())
        self.print_info()

    def print_info(self):
        print("KB DATA INFORMATION")
        print("TOKEN SIZE:{}".format(self.get_token_size()))
        print("ID SIZE:{}".format(len(self)))
        print("TYPE SIZE:{}".format(len(self.types)))
        print("PREDICATE SIZE:{}".format(len(self.predicate)))
        
    def get_id2kb(self):
        print("construct id2kb dict...")
        id2kb = {}
        kbtype = set()
        predicate = set()
        multi_type = []
        with open(self.kb_directory) as f:
            for l in tqdm(f):
                tmp = json.loads(l)
                subject_id = tmp['subject_id']
                subject_alias = list(set([tmp['subject']] + tmp.get('alias', [])))
                subject_alias = [alias.lower() for alias in subject_alias]
                subject_type = [i.lower() for i in tmp['type']]
                kbtype.update(subject_type)
                try:
                    assert(len(tmp['type'])==1)
                except AssertionError:
                    multi_type.append(tmp['type'])
                subject_data = {}
                for i in tmp['data']:
                    predicate.add(i['predicate'].lower())
                    subject_data[i['predicate'].lower()] = i['object'].lower()
                if subject_data:
                    id2kb[subject_id] = {'alias': subject_alias, 'data': subject_data,'type':subject_type}
#         print(multi_type)
        return id2kb,kbtype,predicate

    def get_kb2id(self):
        print("construct kb2id dict...")
        kb2id = {}
        for i,j in self.id2kb.items():
            for k in j['alias']:
                if k not in kb2id:
                    kb2id[k] = []
                kb2id[k].append(i)
        return kb2id
    
    def __len__(self):
        return len(self.id2kb)
    
    def get_token_size(self):
        return len(self.kb)