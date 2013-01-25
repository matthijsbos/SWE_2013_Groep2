import numpy as np
from math import *
import random

# test function for written classes
def test():
  clustering_list = []
  nr_tries = 1000
  best_error=99999999999
  best_clustering = nr_tries+1
  
  #lemma_answers = ["ja","nee","misschien","ja","nee","misschien","nee","ja","misschien","ja","misschien","nee","ja","misschien"]
  
  lemma_answers = ["ja auto kapot","nee auto heel","ja auto kapot","nee auto kapot"
    ,"nee heel","nee","ja voertuig kapot","nee fietser ongeluk","ja fietser auto","ja"]
  
  data=DataClusterer()
  
  for answer in lemma_answers:
    data.add_answer(answer)
  data.tokenize_all()
  data.count_frequency()
  
  for n in range(nr_tries):
    clustering_list.append(N_random())
    for vector in data.token_occurs:
      clustering_list[n].add_vector(vector)
    clustering_list[n].execute()
    if clustering_list[n].error < best_error:
      best_clustering = n
      best_error=clustering_list[n].error
      
  print "---results---"
  print "error is ",best_error
  
  best_clusters = clustering_list[best_clustering].clusters
  text_clusters = []
  for c in range(len(best_clusters)):
    text_clusters.append([])
    for v in range(len(best_clusters[c])):
      vector = best_clusters[c][v]
      for d in data.answers:
        if np.array_equal(d.vector,vector):
          text_clusters[c].append(d.answer)
          break;
  print text_clusters

# contains an answer and its vector representation
class Data():
  answer = ""
  vector = []
  
  def __init__(self):
    self.answer = ""
    self.vector = []

# takes all answers and builds a matrix which shows which words are in which answer
class DataClusterer():
  answers = []
  tokens = []
  token_occurs = []
  
  def __init__(self):
    self.answers = []
    self.tokens = []
    self.token_occurs = []
  
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
      for token in toks:
        if token not in self.tokens:
          self.tokens.append(token)
    # initialize term frequency matrix
    self.token_occurs = np.zeros((len(self.answers),len(self.tokens)))
  
  # counts the frequency of each term in each answer and adds them to the term frequency matrix
  def count_frequency(self):
    for i in range(len(self.answers)):
      toks = self.tokenize_string(self.answers[i].answer)
      for j in range(len(self.tokens)):
        match=False
        for token in toks:
          if token == self.tokens[j]:
            self.token_occurs[i][j] += 1
            self.answers[i].vector.append(1)
            match=True
        if match==False:
          self.answers[i].vector.append(0)

# select some clusters n times and cluster all answers to those clusters
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
    
  # executes all functionalities of this class
  def execute(self):
    self.calc_n()
    self.select_n()
    self.assign_cluster()
    for c in self.clusters:
      self.calc_average_error(c)
    
  # calculate distance between two vectors
  def distance(self,vector1,vector2):
    diff = np.abs(vector1 - vector2)
    length = np.sum(diff)
    return length
  
  # add a vector to this class
  def add_vector(self,vector):
    self.vectors.append(vector)
  
  # determine n
  def calc_n(self):
    self.n = int(log(len(self.vectors[0]))) + 2
    
  # randomly select n clusters
  def select_n(self):
    if self.n < 1:
      self.calc_n()
      if self.n < 1:
        self.n = 1
    a = range(len(self.vectors))
    random.shuffle(a)
    self.selected_indices = a[:self.n]
    for i in self.selected_indices:
      self.selected_vectors.append(self.vectors[i])
      self.clusters.append([])
  
  # assign each answer to a cluster
  def assign_cluster(self):
    for v in self.vectors:
      best_dist = len(v)
      best_selected = 0
      for s in range(len(self.selected_vectors)):
        dist = self.distance(v,self.selected_vectors[s])
        if dist < best_dist:
          best_dist = dist
          best_selected = s
      self.clusters[best_selected].append(v)
   
  # calculate the average error of a cluster and adds this to the total error of this clustering try
  def calc_average_error(self,cluster):
    if cluster == []:
      self.error += 0
    else:
      average = np.average(np.array(cluster),0)
      error = 0
      for c in cluster:
        diff = np.abs(c - average)
        error += np.sum(diff)
      self.error+=error
