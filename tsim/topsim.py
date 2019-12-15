#! /usr/bin/env python3

from .localtyping import *

from functools import partial
import re

from extratools.strtools import str2grams
from extratools.dicttools import invertedindex

from .grammap import createGramMap, updateGramMap, applyGramMap
from .best import findBest
from . import setsimilarity

reSplit = re.compile(r"[_\W]+", re.U)

def str2words(s: str) -> Iterable[str]:
    return (w for w in reSplit.split(s) if len(w) > 0)


class TopSim(object):
    def __init__(
            self,
            sRawStrs: Iterable[str],
            caseSensitive: bool = False,
            mapping: str = "gram", numGrams: int = 2
        ) -> None:
        
        self._str2set_func = lambda s: {
            "gram": partial(str2grams, n=numGrams, pad='\0'),
            "word": str2words,
        }[mapping](s if caseSensitive else s.lower())

        print('starting building grammap...')
        sRawStrSets = [
            list(self._str2set_func(sRawStr))
            for sRawStr in sRawStrs
        ]
        self.sRawStrSets = sRawStrSets
        self.gramMap = createGramMap(sRawStrSets)

        print('gram map infomation:')
        print('keys number:',len(self.gramMap.keys()))
        self.sStrs = [
            applyGramMap(self.gramMap, sRawStrSet)
            for sRawStrSet in sRawStrSets
        ]
        self.sIndex = invertedindex(self.sStrs)


    def search(
            self,
            rRawStr: str,
            k: int = 5, tie: bool = False,worstSim:float = 0.5,
            simFunc: str = "tversky", e: float = 1 / 1000
        ) -> Output:
        rRawStrSet = list(self._str2set_func(rRawStr))
        updateGramMap(self.gramMap, rRawStrSet)

        rStr = applyGramMap(self.gramMap, rRawStrSet)
        # print(rStr)

        upBoundFunc = {
            "overlap": setsimilarity.overlap_upbound,
            "jaccard": setsimilarity.jaccard_upbound,
            "tversky": setsimilarity.tversky_upbound,
        }[simFunc]
        # upBoundFunc = {
        #     "overlap": overlap_upbound,
        #     "jaccard": jaccard_upbound,
        #     "tversky": tversky_upbound,
        # }[simFunc]
        if simFunc == "tversky":
            setsimilarity.e = e
        # print(simFunc)
        return findBest(rStr, self.sStrs, self.sIndex, k, tie, worstSim ,upBoundFunc)
