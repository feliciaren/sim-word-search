#! /usr/bin/env python3

from typing import *

"""
预定义输入输出，使得结果更规范
"""
RawStringSet = List[str]
StringSet = List[int]

GramMap = Dict[str, int]

Index = Dict[int, List[Tuple[int, int]]]

Output = Iterable[Tuple[float, Iterable[int]]]
