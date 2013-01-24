import numpy as np
from math import *
import random

def test():
  clustering_list = []
  nr_tries = 10
  best_error=99999999999
  best_clustering = nr_tries+1
  
  lemma_answers = ["ja auto kapot","nee auto heel","ja auto kapot","nee auto kapot"
    ,"nee heel","nee","ja voertuig kapot","nee fietser ongeluk","ja fietser auto","ja"]
  
  data=DataClusterer()
  
  for answer in lemma_answers:
    data.add_answer(answer)
  data.tokenize_all()
  data.count_frequency()
  
  for n in range(nr_tries):
    clustering_list.append(N_random())
    for vector in data.term_frequency:
      clustering_list[n].add_vector(vector)
    clustering_list[n].execute()
    if clustering_list[n].error < best_error:
      best_clustering = n
      best_error=clustering_list[n].error
      
  print "---results---"
  print best_error
  print best_clustering
  print clustering_list[best_clustering].clusters
    

class Data():
  answer = ""
  vector = []
  
  def __init__(self):
    self.answer = ""
    self.vector = []

class DataClusterer():
  answers = []
  tokens = []
  term_frequency = []
  
  def __init__(self):
    self.answers = []
    self.tokens = []
    self.term_frequency = []
  
  # add answer to list
  def add_answer(self,answer):
    data = Data()
    data.answer = answer.lower()
    # lemmatization goes here
    self.answers.append(data)
  
  # tokenizer placeholder
  def tokenize_string(self,str):
    return str.split()
  
  # tokenize all answers, generate list of tokens and create term frequency matrix
  def tokenize_all(self):
    for str in self.answers:
      toks = self.tokenize_string(str.answer)
      print toks
      for token in toks:
        if token not in self.tokens:
          self.tokens.append(token)
    # initialize term frequency matrix
    self.term_frequency = np.zeros((len(self.answers),len(self.tokens)))
  
  # counts the frequency of each term in each answer and adds them to the term frequency matrix
  def count_frequency(self):
    for i in range(len(self.answers)):
      toks = self.tokenize_string(self.answers[i].answer)
      for j in range(len(self.tokens)):
        match=False
        for token in toks:
          if token == self.tokens[j]:
            self.term_frequency[i][j] = 1
            self.answers[i].vector.append(1)
            match=True
        if match==False:
          self.answers[i].vector.append(0)
    print "---begin content of DataClusterer---"
    print self.term_frequency
    print self.tokens
    for data in self.answers:
      print data.vector
    print "---end content of DataClusterer---"
    
class N_random():
  n = 0
  vectors = []
  set_n = 0
  selected_indices = []
  selected_vectors = []
  clusters = []
  error=0
  
  def __init__(self):
    self.n = 0
    self.vectors = []
    self.set_n = 0
    self.selected_indices = []
    self.selected_vectors = []
    self.clusters = []
    self.error = 0
    
  def execute(self):
    self.calc_n()
    self.select_n()
    self.assign_cluster()
    for c in self.clusters:
      self.calc_average_error(c)
    print "---begin clusters---"
    print self.clusters
    print "---end clusters---"
    
  def distance(self,vector1,vector2):
    #vector1 = self.vectors[q1]
    #vector2 = self.vectors[q2]
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
      while a in self.selected_indices:
        a = random.randint(0,len(self.vectors)-1)
      self.selected_indices.append(a)
      self.selected_vectors.append(self.vectors[a])
      self.clusters.append([])
    print "---begin selected vectors---"
    print self.selected_vectors
    print "---end selected vectors---"
  
  def assign_cluster(self):
    for v in self.vectors:
      best_dist = 0
      best_selected = 0
      for s in range(len(self.selected_vectors)):
        dist = self.distance(v,self.selected_vectors[s])
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
