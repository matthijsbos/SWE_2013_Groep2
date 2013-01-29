import numpy as np
from math import *
import random
import lang_parser
import sys

# test function for the classes, also shows basic way to use clusterer
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
    self.best_n = None
  
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
    
    # add lemmatized answers to data analyzer
    for i in range(len(lemma_answers)):
      self.data.add_answer(lemma_answers[i],self.answers[i])
    self.data.tokenize_all()
    self.data.count_frequency()
    
    # determine best cluster found in n tries
    for n in range(self.nr_tries):
      self.clustering_list.append(N_random())
      if self.n_clusters != 0:
        self.clustering_list[n].set_n(self.n_clusters)
      for data in self.data.answers:
        self.clustering_list[n].add_data(data)
      self.clustering_list[n].execute()
      if self.clustering_list[n].error < self.best_error:
        self.best_clustering = n
        self.best_error=self.clustering_list[n].error
    
    # change best cluster into list of string lists for easier reading
    self.best_n = self.clustering_list[self.best_clustering]
    best_clusters = self.best_n.clusters
    text_clusters = []
    for c in range(len(best_clusters)):
      text_clusters.append([])
      for v in range(len(best_clusters[c])):
        data = best_clusters[c][v]
        text_clusters[c].append(data.string)
    return text_clusters
  
  # remove cluster with index 'index' and rerun clustering
  def remove_cluster(self,index):
    # remove and reset some data
    self.best_n.selected_indices.pop(index)
    self.best_n.selected_data.pop(index)
    self.best_n.clusters = []
    self.best_n.error = 0
    for a in range(len(self.best_n.selected_indices)):
      self.best_n.clusters.append([])
    
    # rerun clustering
    self.best_n.assign_cluster()
    for c in self.best_n.clusters:
      self.best_n.calc_average_error(c)
    
    # form human readable output
    best_clusters = self.best_n.clusters
    text_clusters = []
    for c in range(len(best_clusters)):
      text_clusters.append([])
      for v in range(len(best_clusters[c])):
        data = best_clusters[c][v]
        text_clusters[c].append(data.string)
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
    self.data = []
    self.set_n = 0
    self.selected_indices = []
    self.selected_data = []
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
    print vector1,vector2
    diff = np.abs(np.array(vector1) - np.array(vector2))
    length = np.sum(diff)
    return length
    
  # add data element to class
  def add_data(self,data):
    self.data.append(data)
  
  # let user set a n
  def set_n(self,n):
    self.static_n = n
  
  # determine n
  def calc_n(self):
    if self.static_n == False:
      self.n = min((int(log(len(self.data[0].vector),2)) + 1),(int(log(len(self.data),2)) + 1))
  
  # randomly select n clusters
  def select_n(self):
    if self.n < 1:
      self.calc_n()
      if self.n < 1:
        self.n = 1
    a = range(len(self.data))
    random.shuffle(a)
    self.selected_indices = a[:self.n]
    for i in self.selected_indices:
      self.selected_data.append(self.data[i])
      self.clusters.append([])
  
  # assign each answer to a cluster
  def assign_cluster(self):
    for d in self.data:
      best_dist = len(d.vector)
      best_selected = 0
      for s in range(len(self.selected_data)):
        dist = self.distance(d.vector,self.selected_data[s].vector)
        if dist < best_dist:
          best_dist = dist
          best_selected = s
      self.clusters[best_selected].append(d)
  
  # calcluates the average vector of a cluster
  def average(self,cluster):
    sum = []
    for a in range(len(cluster[0].vector)):
      sum.append(0)
    sum = np.array(sum)
    for c in cluster:
      sum += np.array(c.vector)
    sum /= len(cluster)
    return sum
  
  # calculate the average error of a cluster and adds this to the total error of this clustering try
  def calc_average_error(self,cluster):
    if cluster == []:
      self.error += 0
    else:
      avg = self.average(cluster)
      error = 0
      for c in cluster:
        diff = np.abs(c.vector - avg)
        error += np.sum(diff)
      self.error+=error
