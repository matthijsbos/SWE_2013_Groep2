import numpy as np
from math import *
import random
import lang_parser
import sys

def test():
  clusterer = Clusterer()
  answer_strings=["yes, the car crashes","yes, the car does crash","no, it stays whole","yes, the cyclist gets run over by the car",
    "yes, the cyclist gets run over by the vehicle","yes, the cyclist gets into an accident"]
  for a in answer_strings:
    clusterer.add_answer(a)
  #clusterer.change_nr_tries(3)
  print clusterer.run_clustering()

# initialize an instance of this class to do clustering
class Clusterer():
  def __init__(self):
    self.answers = []
    self.data = DataClusterer()
    self.best_error = sys.maxsize
    self.nr_tries = 10
    self.best_clustering = self.nr_tries + 1
    self.clustering_list = []
    self.n_clusters = 0
  
  # add answer to cluster module
  def add_answer(self,answer):
    self.answers.append(answer)
  
  # sets a number of clusters to add answers to
  def set_number_of_clusters(self,nr):
    self.n_clusters = nr
    
  # change number of tries to search for best cluster
  def change_nr_tries(self,new_value):
    self.nr_tries = new_value
  
  # runs clustering over the data
  def run_clustering(self):
    lp = lang_parser.LanguageParser('en',self.answers)
    lemma_answers = lp.get_keywords()
    
    for i in range(len(lemma_answers)):
      self.data.add_answer(lemma_answers[i],self.answers[i])
    self.data.tokenize_all()
    self.data.count_frequency()
    
    for n in range(self.nr_tries):
      self.clustering_list.append(N_random())
      if self.n_clusters != 0:
        self.clustering_list[n].set_n(self.n_clusters)
      for vector in self.data.token_occurs:
        self.clustering_list[n].add_vector(vector)
      self.clustering_list[n].execute()
      if self.clustering_list[n].error < self.best_error:
        self.best_clustering = n
        self.best_error=self.clustering_list[n].error
    
    best_clusters = self.clustering_list[self.best_clustering].clusters
    text_clusters = []
    for c in range(len(best_clusters)):
      text_clusters.append([])
      for v in range(len(best_clusters[c])):
        vector = best_clusters[c][v]
        for d in self.data.answers:
          if np.array_equal(d.vector,vector):
            text_clusters[c].append(d.string)
            break;
    return text_clusters

# contains an answer and its vector representation
class Data():  
  def __init__(self):
    self.answer = ""
    self.string = ""
    self.vector = []

# takes all answers and builds a matrix which shows which words are in which answer
class DataClusterer():
  def __init__(self):
    self.answers = []
    self.tokens = []
    self.token_occurs = []
  
  # add answer to list
  def add_answer(self,answer,string):
    data = Data()
    data.answer = answer
    data.string = string
    # lemmatization goes here
    self.answers.append(data)
  
  # tokenizer placeholder
  def tokenize_string(self,str):
    return str.split()
  
  # tokenize all answers, generate list of tokens and create term frequency matrix
  def tokenize_all(self):
    for str in self.answers:
      #toks = self.tokenize_string(str.answer)
      print str.answer
      for token in str.answer:
        if token not in self.tokens:
          self.tokens.append(token)
    # initialize term frequency matrix
    self.token_occurs = np.zeros((len(self.answers),len(self.tokens)))
  
  # counts the frequency of each term in each answer and adds them to the term frequency matrix
  def count_frequency(self):
    for i in range(len(self.answers)):
      #toks = self.tokenize_string(self.answers[i].answer)
      toks = self.answers[i].answer
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
  def __init__(self):
    self.n = 0
    self.vectors = []
    self.set_n = 0
    self.selected_indices = []
    self.selected_vectors = []
    self.clusters = []
    self.error = 0
    self.static_n = False
    
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
  
  # let user set a n
  def set_n(self,n):
    self.static_n = n
  
  # determine n
  def calc_n(self):
    if self.static_n == False:
      self.n = min((int(log(len(self.vectors[0]),2)) + 1),(int(log(len(self.vectors),2)) + 1))
  
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
