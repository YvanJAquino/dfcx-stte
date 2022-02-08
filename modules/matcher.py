import os
import time
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

from .stringpipe import StringPipeline

class NameMatcher:

   DEFAULT_CONFIG = dict(
      source_file = '../data/full_names.json',
      min_df = 1,
      n_neighbors = 5,
      out_file = '../ai-models/matcher.mdl'
   )

   def __init__(self, **kwargs):      
      self.source_file = kwargs.get('source_file') or self.DEFAULT_CONFIG['source_file']
      self.min_df      = kwargs.get('min_df') or self.DEFAULT_CONFIG.get('min_df')
      self.n_neighbors = kwargs.get('n_neighbors') or self.DEFAULT_CONFIG.get('n_neighbors')
      self.out_file    = kwargs.get('out_file') or self.DEFAULT_CONFIG.get('out_file')

      self.perf_stats = {}
      
      self.source = self._source()
      self.analyzer = self._analyzer()
      self.vectorizer = TfidfVectorizer(min_df=self.min_df, analyzer=self.analyzer)
      self.tfidf = self._tfidf()
      self.kneighbors = self._kneighbors()
      
   def timeit(self, func, name, *args, **kwargs):
      start = time.perf_counter()
      res = func(*args, **kwargs)
      delta = time.perf_counter() - start
      self.perf_stats[name] = delta
      return res


   def _source(self):
      with open(self.source_file) as src:
         _src = json.load(src)
         
         if not isinstance(_src, list):
            raise TypeError("Source data must be in list format.")
         
         return _src

   def _analyzer(self):
      with StringPipeline() as (pipe, ops):
         (
            pipe
               >> ops.lower()
               >> ops.remove_punctuation()
               >> ops.cum_ngrams()
         )
         return pipe

   def _tfidf(self):
      return self.vectorizer.fit_transform(self.source)

   def _kneighbors(self):
      return NearestNeighbors(n_neighbors=self.n_neighbors, n_jobs=-1, metric='cosine').fit(self.tfidf)

   def match(self, target: str):
      vectorized = self.vectorizer.transform([target])
      distances, indices = self.kneighbors.kneighbors(vectorized)
      records = [
         {
            'target':target,
            'source': self.source[idx],
            'similarity': 1-dist.item()
         }
         for dist, idx in zip(distances[0], indices[0])
      ]
      records.sort(key=lambda d: d['similarity'], reverse=True)
      return records

   def dump(self):
      joblib.dump(self, self.out_file)
      print(f'Model dumped to: {self.out_file}')

   @staticmethod
   def from_file(path: str):
      return joblib.load(path)


import argparse
import yaml


class NameMatcherCLI:

   def __init__(self):
      self.parser = argparse.ArgumentParser()
      self.parser.add_argument('-c', '--config', default='config.yaml')
      self.parser.add_argument('-f', '--format', default='yaml')
      self.parser.add_argument('-p', '--print', action='store_true')

   def __call__(self):
      args = self.parser.parse_args()
      config_path = args.config
      config_format = args.format
      with open(config_path) as src:
         if config_format == 'yaml':
            config = yaml.load(src, Loader=yaml.FullLoader)
         elif config_format == 'json':
            config = json.load(src)
      
      if args.print:
         print(json.dumps(config, indent=2))
      
      return config


if __name__ == '__main__':
   args = NameMatcherCLI()
   config = args()
   matcher = NameMatcher(**config)
   matcher.dump()
