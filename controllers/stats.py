from flask import escape, render_template, g
from clusterer import *

class Stats():
    @staticmethod
    def render():
      #clusters is 2d array van strings
      return render_template('iets.html',clusters=clusterer.run_clustering())