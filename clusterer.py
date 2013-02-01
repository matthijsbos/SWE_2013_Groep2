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
  print clusterer.remove_cluster(0)

# error class for cluster module
class ClusterError(Exception):
  def __init__(self,msg):
    self.msg = msg
  
  def __str__(self):
    return repr(self.msg)

# initialize an instance of this class to do clustering
class Clusterer():
  def __init__(self):
    self.answers = []
    self.data = _DataClusterer()
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
    if nr < 1:
      raise ClusterError('set_number_of_clusters argument must be at least 1')
    self.n_clusters = nr
    
  # change number of tries to search for best cluster
  def change_nr_tries(self,new_value):
    if new_value < 1:
      raise ClusterError('change_nr_tries argument nmust be at least 1')
    self.nr_tries = new_value
  
  # runs clustering over the data, run this function only once for a clusterer instance
  def run_clustering(self):
    if len(self.answers) < 1:
      raise ClusterError('you need to add at least 1 answer to Clusterer before calling run_clustering')
    lp = lang_parser.LanguageParser('en',self.answers)
    lp.detect_language()
    lemma_answers = lp.get_keywords()
    
    # add lemmatized answers to data analyzer
    for i in range(len(lemma_answers)):
      self.data.add_answer(lemma_answers[i],self.answers[i])
    self.data.tokenize_all()
    self.data.count_frequency()
    
    # determine best cluster found in n tries
    for n in range(self.nr_tries):
      self.clustering_list.append(_N_random())
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
    if len(self.best_n.selected_indices) < 2:
      raise ClusterError('removing this cluster would cause the clusterer to work with 0 clusters')
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

# initialize an instance of this class to do clustering with stars

class ClustererStars(Clusterer):
  def __init__(self):
    self.answers = []
    self.stars = []
    self.data = _DataClusterer()
    self.best_error = sys.maxsize
    self.nr_tries = 10
    self.best_clustering = self.nr_tries + 1
    self.clustering_list = []
    self.n_clusters = 0
    self.best_n = None
  
  # add answer to cluster module
  def add_answer(self,answer,stars):
    self.answers.append(answer)
    self.stars.append(stars)
    
  # runs clustering over the data, run this function only once for a clusterer instance
  def run_clustering(self):
    if len(self.answers) < 1:
      raise ClusterError('you need to add at least 1 answer to Clusterer before calling run_clustering')
    lp = lang_parser.LanguageParser('en',self.answers)
    lp.detect_language()
    lemma_answers = lp.get_keywords()
    
    # add lemmatized answers to data analyzer
    for i in range(len(lemma_answers)):
      self.data.add_answer(lemma_answers[i],self.answers[i],self.stars[i])
    self.data.tokenize_all()
    self.data.count_frequency()
    
    # determine best cluster found in n tries
    for n in range(self.nr_tries):
      self.clustering_list.append(_N_random())
      if self.n_clusters != 0:
        self.clustering_list[n].set_n(self.n_clusters)
      for data in self.data.answers:
        self.clustering_list[n].add_data(data)
      self.clustering_list[n].execute()
      if self.clustering_list[n].error < self.best_error:
        self.best_clustering = n
        self.best_error=self.clustering_list[n].error
    
    # generate info for cluster
    self.best_n = self.clustering_list[self.best_clustering]
    best_clusters = self.best_n.clusters
    cluster_info = []
    for cluster in best_clusters:
      best_stars = 0
      best_str = ""
      worst_stars = 6
      worst_str = ""
      number = 0
      avg_stars = 0
      for data in cluster:
        if data.stars > best_stars:
          best_stars = data.stars
          best_str = data.string
        if data.stars < worst_stars:
          worst_stars = data.stars
          worst_str = data.string
        number += 1
        avg_stars += data.stars
      if number != 0:
        avg_stars /= number
      cluster_info.append([best_stars,best_str,worst_stars,worst_str,number,avg_stars])
    return cluster_info

  # remove cluster with index 'index' and rerun clustering
  def remove_cluster(self,index):
    if len(self.best_n.selected_indices) < 2:
      raise ClusterError('removing this cluster would cause the clusterer to work with 0 clusters')
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
    
    # generate info for cluster
    self.best_n = self.clustering_list[self.best_clustering]
    best_clusters = self.best_n.clusters
    cluster_info = []
    for cluster in best_clusters:
      best_stars = 0
      best_str = ""
      worst_stars = 6
      worst_str = ""
      number = 0
      avg_stars = 0
      for data in cluster:
        if data.stars > best_stars:
          best_stars = data.stars
          best_str = data.string
        if data.stars < worst_stars:
          worst_stars = data.stars
          worst_str = data.string
        number += 1
        avg_stars += data.stars
      if number != 0:
        avg_stars /= number
      cluster_info.append([best_stars,best_str,worst_stars,worst_str,number,avg_stars])
    return cluster_info
    
# contains an answer and its vector representation
class _Data():  
  def __init__(self):
    self.answer = ""
    self.string = ""
    self.vector = []
    self.stars = 0

# takes all answers and builds a matrix which shows which words are in which answer
class _DataClusterer():
  def __init__(self):
    self.answers = []
    self.tokens = []
    self.token_occurs = []
  
  # add answer to list
  def add_answer(self,answer,string,stars=0):
    data = _Data()
    data.answer = answer
    data.string = string
    data.stars = stars
    self.answers.append(data)
  
  # tokenize all answers, generate list of tokens and create term frequency matrix
  def tokenize_all(self):
    for str in self.answers:
      for token in str.answer:
        if token not in self.tokens:
          self.tokens.append(token)
    # initialize term frequency matrix
    self.token_occurs = np.zeros((len(self.answers),len(self.tokens)))
  
  # counts the frequency of each term in each answer and adds them to the term frequency matrix
  def count_frequency(self):
    for i in range(len(self.answers)):
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
class _N_random():  
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
