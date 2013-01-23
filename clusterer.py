import numpy as np
from math import *
import random

def test():
  clustering_list = []
  nr_tries = 10
  best_error=99999999999
  best_clustering = nr_tries+1
  
  lemma_answers = ["ja","nee"]
  
  data=Data()
  
  for answer in lemma_answers:
    data.add_answer(answer)
  data.tokenize_all()
  data.count_frequency()
  
  for n in range(nr_tries):
    clustering_list.append(N_random())
    for vector in range(len(data.term_frequency)):
      clustering_list[n].add_vector(vector)
    clustering_list[n].execute()
    if clustering_list[n].error < best_error:
      best_clustering = n
      best_error=clustering_list[n].error
      
  print best_error
  print best_clustering
    

class Data():
  answers = []
  tokens = []
  term_frequency = []
  
  def __init__(self):
    self.answers = []
    self.tokens = []
    self.term_frequency = []
  
  # add answer to list
  def add_answer(self,answer):
    # lemmatization goes here
    self.answers.append(answer.lower())
  
  # tokenizer placeholder
  def tokenize_string(self,str):
    return str.split(' .,')
  
  # tokenize all answers, generate list of tokens and create term frequency matrix
  def tokenize_all(self):
    for str in self.answers:
      toks = self.tokenize_string(str)
      for token in toks:
        if token not in self.tokens:
          self.tokens.append(token)
    # initialize term frequency matrix
    self.term_frequency = np.zeros((len(self.answers),len(self.tokens)))
  
  # counts the frequency of each term in each answer and adds them to the term frequency matrix
  def count_frequency(self):
    for i in range(len(self.answers)):
      toks = self.tokenize_string(self.answers[i])
      for token in toks:
        for k in range(len(self.tokens)):
          if token == k:
            self.term_frequency[i][j] = 1
    
class N_random():
  n = 0
  vectors = []
  set_n = 0
  selected = []
  clusters = []
  error=0
  
  def __init__(self):
    self.n = 0
    self.vectors = []
    self.selected = []
    self.clusters = []
    
  def execute(self):
    self.calc_n()
    self.select_n()
    self.assign_cluster()
    for c in self.clusters:
      self.calc_average_error(c)
    
  def distance(self,q1,q2):
    vector1 = self.vectors[q1]
    vector2 = self.vectors[q2]
    result = vector1 * vector2
    length = np.sum(result)
    return length
  
  def add_vector(self,vector):
    self.vectors.append(vector)
  
  def calc_n(self):
    self.n = int(log(len(self.vectors)))
    
  def select_n(self):
    if self.n < 1:
      self.calc_n()
      if self.n < 1:
        self.n = 1
    for i in range(self.n):
      a = random.randint(0,len(self.vectors)-1)
      while self.vectors[a] in self.selected:
        a = random.randint(0,len(self.vectors)-1)
      self.selected.append(self.vectors[a])
      self.clusters.append([])
  
  def assign_cluster(self):
    for v in self.vectors:
      best_dist = 0
      best_selected = 0
      for s in range(len(self.selected)):
        dist = self.distance(v,self.selected[s])
        if dist > best_dist:
          best_dist = dist
          best_selected = s
      self.clusters[best_selected].append(v)
      
  def calc_average_error(self,cluster):
    average = np.average(np.array(cluster),0)
    error = 0
    for c in cluster:
      diff = np.abs(c - average)
      error += np.sum(diff)
    self.error=error
