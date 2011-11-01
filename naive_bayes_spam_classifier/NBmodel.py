import pickle
import os
import string
import collections
import math
import sys
import numpy
from itertools import izip

cached_files = {}
cached_sets = {}
cached_maps = {}

#########################################

# Converts an e-mail file, given a features file name, into 
# a feature vector.
def munge_Boolean(email_filename,features_filename):
    email_file = open(email_filename, "r")

    if features_filename in cached_files:
        feature_list = cached_files[features_filename]
        feature_map = cached_maps[features_filename]
        feature_set = cached_sets[features_filename]
    else:
        feature_list = pickle.load(open(features_filename, "rb"))
        feature_map = {}
        feature_set = set(feature_list)

        for k,v in enumerate(feature_list):
            feature_map[v] = k

        cached_files[features_filename] = feature_list
        cached_sets[features_filename] = feature_set
        cached_maps[features_filename] = feature_map

    weight_vector = [False]*len(feature_list)
    
    for l in email_file.readlines():
        l.lower()
        l = filter(lambda letter: (letter.isalpha() or letter == ' '), l)
        l = filter(lambda word: len(word) > 3, l.split())
        for word in l:
            if word in feature_set:
                weight_vector[feature_map[word]] = True

    return weight_vector

def NBclassify_Boolean(example,model,cost_ratio):
    # Calculate the probability that, given each word in the
    # model's frequency list, this example is spam.

    prHam = model.ham_instance_count/float(model.instance_count)
    prSpam = model.spam_instance_count/float(model.instance_count)
    
    # Construct ham term
    # posterior(ham) = P(ham) * P(T_1 | ham) * P(T_2 | ham) / evidence
    # posterior(spam) = P(spam) * P(T_1 | spam) * P (T_2 | spam) / evidence

    # Construct series (P(T_1 | ham) * P(T_2 | ham))
    hamTerm = prHam
    for i,termCount in enumerate(model.ham_frequency_vector):
        if example[i] == 1:
            hamTerm *= termCount/float(model.ham_instance_count)
        else:
            hamTerm *= (model.ham_instance_count - termCount)/float(model.ham_instance_count)

    # Construct spam term

    spamTerm = prSpam
    for i,termCount in enumerate(model.spam_frequency_vector):
        if example[i] == 1:
            spamTerm *= termCount/float(model.spam_instance_count)
        else:
            spamTerm *= (model.spam_instance_count - termCount)/float(model.spam_instance_count)

    # Encourage posterior to be more often classified as ham than spam by
    # the cost_ratio
    
    hamTerm *= cost_ratio

    return 1 if spamTerm > hamTerm else 0

#########################################

def get_files(path):
    for f in os.listdir(path):
        f = os.path.abspath( os.path.join(path, f ) )
        if os.path.isfile( f ):
            yield f


class NaiveBayesModel:
    
    def __init__(self, features_file, model_file):
        self.features = pickle.load(open(features_file,'rb'))
        self.model = pickle.load(open(model_file,'rb'))

    def test(self, spam_dir, ham_dir, cost_ratio):
        N = 0
        loss = 0.
        for f in get_files(spam_dir):
            N += 1
            classification = self.classify(self.munge(f),cost_ratio)
            if not (classification==1):
                loss += 1
    
        for f in get_files(ham_dir):
            N += 1
            classification = self.classify(self.munge(f),cost_ratio)
            if not (classification==0):
                loss += cost_ratio
        
        print "Classifier average loss: %f" % (loss/N)


class NB_Boolean(NaiveBayesModel):
    def classify(self,example,cost_ratio):
        return NBclassify_Boolean(example,self.model,cost_ratio)
        
    def munge(self,email_file):
        return munge_Boolean(email_file,self.features)

# Data structure to hold Boolean classifier
# It's simply a container data structure to describe Boolean lists and counts.

class NaiveBayesClassifier():
    def __init__(self):
        self.spam_frequency_vector = [0]
        self.ham_frequency_vector = [0]
        self.instance_count = 0
        self.spam_instance_count = 0
        self.ham_instance_count = 0

#########################################
        
def train_boolean_classifier(spam_directory, ham_directory, features_filename):
    # features_filename consists of a pickled list of features
    
    features = pickle.load(open(features_filename, "rb"))
    
    model = NaiveBayesClassifier()
    model.spam_frequency_vector = [0]*len(features)
    model.ham_frequency_vector = [0]*len(features)
        
    # Calculate spam instances
    print "Calculating spam instances..."
    for filename in get_files(spam_directory):
        print ".",
        for i, value in enumerate(munge_Boolean(filename, features_filename)):
            model.spam_frequency_vector[i] += value
        model.spam_instance_count += 1
        model.instance_count += 1

    # Calculate ham instances
    print "Calculating ham instances..."
    for filename in get_files(ham_directory):
        print ".",
        for i, value in enumerate(munge_Boolean(filename, features_filename)):
            model.ham_frequency_vector[i] += value
        model.ham_instance_count += 1
        model.instance_count += 1

    return model

def create_boolean_model_file():
    boolean_model_file = open("Boolean.model", "a+")
    boolean_model = train_boolean_classifier("train/spam", "train/ham", "Boolean.features")
    pickle.dump(boolean_model, boolean_model_file)
    boolean_model_file.close()

def test(cost_ratio):
    boolean_model = pickle.load(open("Boolean.model", "r"))

    for filename in get_files("xvalidation/ham/4"):
        ex = munge_Boolean(filename, "Boolean.features")
        print NBclassify_Boolean(ex, boolean_model, cost_ratio)
