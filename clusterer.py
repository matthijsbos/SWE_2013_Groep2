import numpy as np
from Math import *
import random

clustering_list = []
nr_tries = 10
best_error=99999999999
best_clustering = nr_tries+1

data=Data()

for answer in lemma_answers
  data.add_answer(answer)
data.tokenize_all()
data.count_frequency()

for n in range(nr_tries):
  clustering_list[n]=N_random()
  for vector in range(len(data.term_frequency))
    clustering_list[n].add_vector(vector)
  clustering_list[n].execute()
  if clustering_list[n].error < best_error:
    best_clustering = n
    best_error=clustering_list[n].error
    

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
    for str in answers:
      toks = tokenize_string(str)
      for token in toks:
        if token not in tokens:
          self.tokens.append(t)
    # initialize term frequency matrix
    self.term_frequency = np.zeros((len(answers),len(tokens)))
  
  # counts the frequency of each term in each answer and adds them to the term frequency matrix
  def count_frequency(self):
    for i in range(len(answers)):
      toks = tokenize_string(answers[i])
      for token in toks:
        for k in range(len(tokens)):
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
    
  def execute():
    calc_n()
    select_n()
    assign_cluster()
    calc_average_error()
    
  def distance(q1,q2):
    vector1 = term_frequency[q1]
    vector2 = term_frequency[q2]
    result = vector1 * vector2
    length = np.sum(result)
    return length
  
  def add_vector(self,vector):
    self.vectors.append(vector)
  
  def calc_n(self):
    self.n = int(log(len(vectors)))
    
  def select_n(self):
    if n < 1:
      calc_n()
      if n < 1:
        self.n = 1
    for i in range(n):
      a = random.randint(0,len(vectors)-1)
      while vectors[a] in selected:
        a = random.randint(0,len(vectors)-1)
      self.selected.append(vectors[a])
      self.clusters.append([])
  
  def assign_cluster(self):
    for v in vectors:
      best_dist = 0
      best_selected = 0
      for s in selected:
        dist = distance(v,s)
        if dist > best_dist:
          best_dist = dist
          best_selected = s
      self.clusters[best_selected].append(v)
      
  def calc_average_error(cluster):
    average = np.average(np.array(cluster),0)
    error = 0
    for c in cluster:
      diff = np.abs(c - average)
      error += np.sum(diff)
    self.error=error
