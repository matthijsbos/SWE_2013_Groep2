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
  print clustering_list[best_clustering].clusters


class Data():
  name=""
  text=""
  vector=[]
  
  def __init__(self):
    self.name=""
    self.text=""
    self.vector=[]


class Vector_creation():
  answers = []
  tokens = []
  term_frequency = []
  
  def __init__(self):
    self.answers = []
    self.tokens = []
    self.term_frequency = []
  
  # add answer to list
  def add_answer(self,answer):
    self.answers.append(answer)
  
  # tokenizer placeholder
  def tokenize_string(self,str):
    return str.split()
  
  # tokenize all answers, generate list of tokens and create term frequency matrix
  def tokenize_all(self):
    for n in range(len(answers)):
      tokens = self.tokenize_string(answers[n].text)
      for token in tokens:
        if token not in self.tokens:
          self.tokens.append(token)
    # initialize term frequency matrix
    self.term_frequency = np.zeros((len(self.answers),len(self.tokens)))
  
  # counts the frequency of each term in each answer and adds them to the term frequency matrix
  def count_frequency(self):
    for i in range(len(self.answers)):
      tokens = self.tokenize_string(self.answers[i])
      for token in tokens:
        for j in range(len(self.tokens)):
          if token == self.tokens[j]:
            self.term_frequency[i][j] = 1
    print self.term_frequency
    print self.tokens
    
class N_random():
  n = 0
  answers = []
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
    print self.clusters
    
  def distance(self,q1,q2):
    vector1 = self.answers[q1].vector
    vector2 = self.answers[q2].vector
    result = vector1 * vector2
    length = np.sum(result)
    return length
  
  def add_vector(self,answer):
    self.answers.append(answer)
  
  def calc_n(self):
    self.n = int(log(len(self.vectors)))
    
  def select_n(self):
    if self.n < 1:
      self.calc_n()
      if self.n < 1:
        self.n = 1
    for i in range(self.n):
      a = random.randint(0,len(self.answers)-1)
      while self.answers[a].vector in self.selected:
        a = random.randint(0,len(self.answers)-1)
      self.selected.append(self.answers[a].vector)
      self.clusters.append([])
  
  def assign_cluster(self):
    for n in range(len(self.answers)):
    vector=self.answers[n].vector
      best_dist = 0
      best_selected = 0
      for s in range(len(self.selected)):
        dist = self.distance(vector,self.selected[s])
        if dist > best_dist:
          best_dist = dist
          best_selected = s
      self.clusters[best_selected].append(self.answers[n])
      
  def calc_average_error(self,cluster):
    #average moet opnieuw gaat compiler fout maken
    average = np.average(np.array(cluster),0)
    error = 0
    for n in range(len(cluster)):
      vector=cluster[n].vector
      diff = np.abs(c - average)
      error += np.sum(diff)
    self.error=error
