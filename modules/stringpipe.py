# Copyright 2022 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import string


class StringOperator:

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    # do calls the functions on either the string or each string element of a given list.
    def do(self, inp):
        
        if isinstance(inp, str):
            return self.func(inp, *self.args, **self.kwargs)
        elif isinstance(inp, list):
            return [self.func(i, *self.args, **self.kwargs) for i in inp]

    @classmethod
    def lower(cls):
        return cls(str.lower)

    @classmethod
    def split(cls, sep):
        return cls(str.split, sep)

    @classmethod
    def strip(cls, chars = ''):
        return cls(str.strip, chars)

    @classmethod
    def replace(cls, old, new, count=0):
        if count == 0:
            return cls(str.replace, old, new)
        else:
            return cls(str.replace, old, new, count)

    @classmethod
    def remove_punctuation(cls):
        return cls(str.translate, str.maketrans('', '', string.punctuation))

    @staticmethod
    def to_ngrams(s, n):
        return {s[i:i+n] for i in range(len(s)-(n-1))}

    @classmethod
    def ngrams(cls, n=3):       
        return cls(StringOperator.to_ngrams, n)

    @staticmethod
    def to_cum_ngrams(s, n, m):
        all_ngrams = set()
        for x in range(m, n+1):
            all_ngrams = all_ngrams.union(StringOperator.to_ngrams(s, x))
        return all_ngrams

    @classmethod
    def cum_ngrams(cls, n=3, m=2):
        return cls(StringOperator.to_cum_ngrams, n, m) 


class StringPipeline:   

    def __init__(self):
        self.ops = []

    def do(self, inp):
        out = inp
        for op in self.ops:
            out = op.do(out)
        return out  

    def __call__(self, inp):
        return self.do(inp)

    def __rshift__(self, op):
        
        if not isinstance(op, StringOperator):
            raise TypeError
        
        self.ops.append(op)
        return self 

    def __enter__(self):
        return self, StringOperator
    
    def __exit__(self, exc_val, exc_type, exc_traceback):
        return self

