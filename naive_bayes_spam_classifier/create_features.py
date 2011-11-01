import os
import shutil
import collections
import pickle

# Need to observe features at least FEATURE_OBSERVATION_THRESHOLD times before 
# we consider it as a feature.
FEATURE_OBSERVATION_THRESHOLD = 4
# Prune features whose length is less than FEATURE_LENGTH_THRESHOLD.
FEATURE_LENGTH_THRESHOLD = 3

def get_files(path):
    for f in os.listdir(path):
        f = os.path.abspath( os.path.join(path, f ) )
        if os.path.isfile( f ):
            yield f

hamFeatures = collections.defaultdict(int)
hamInstances = 0
spamFeatures = collections.defaultdict(int)
spamInstances = 0

for setindex in xrange(1,11):
    print "Running HAM feature selection on set " + str(setindex)
    for filename in get_files("xvalidation/ham/" + str(setindex)):
        hamInstances += 1
        f = open(filename, "r")
        filefeatures = set()
        for l in f.readlines():
            l.lower()
            l = filter(lambda letter: (letter.isalpha() or letter == ' '), l)
            l = filter(lambda word: len(word) > FEATURE_LENGTH_THRESHOLD, l.split())
            for word in l:
                filefeatures.add(word)
        for word in filefeatures:
            hamFeatures[word] += 1

print "Beginning to prune HAM feature selection."

prunedHamFeatures = collections.defaultdict(int)
for k in hamFeatures:
    if hamFeatures[k] > FEATURE_OBSERVATION_THRESHOLD:
        prunedHamFeatures[k] = hamFeatures[k]

hamFeatures = prunedHamFeatures

for setindex in xrange(1,11):
    print "Running SPAM feature selection on set " + str(setindex)
    for filename in get_files("xvalidation/spam/" + str(setindex)):
        spamInstances += 1
        f = open(filename, "r")
        filefeatures = set()
        for l in f.readlines():
            l.lower()
            l = filter(lambda letter: (letter.isalpha() or letter == ' '), l)
            l = filter(lambda word: len(word) > FEATURE_LENGTH_THRESHOLD, l.split())
            for word in l:
                filefeatures.add(word)
        for word in filefeatures:
            spamFeatures[word] += 1

prunedSpamFeatures = collections.defaultdict(int)

for k in spamFeatures:
    if spamFeatures[k] > FEATURE_OBSERVATION_THRESHOLD:
        prunedSpamFeatures[k] = spamFeatures[k]

spamFeatures = prunedSpamFeatures

featuresToRemove = set()
for feature in hamFeatures:
    if (hamFeatures[feature]/float(hamInstances) < 
        3*spamFeatures[feature]/float(spamInstances)):
        featuresToRemove.add(feature)
        print "Removing feature \"" + feature + "\" - comparison " + str(hamFeatures[feature]/float(hamInstances)) + " versus " + str(spamFeatures[feature]/float(spamInstances))

for f in featuresToRemove:
    del hamFeatures[f]

featuresToRemove = set()
for feature in spamFeatures:
    if (spamFeatures[feature]/float(spamInstances) < 
        3*hamFeatures[feature]/float(hamInstances)):
        featuresToRemove.add(feature)
        print "Removing feature \"" + feature + "\" - comparison " + str(spamFeatures[feature]/float(spamInstances)) + " versus " + str(hamFeatures[feature]/float(hamInstances))

for f in featuresToRemove:
    del spamFeatures[f]

# Dump the features as a picked list of files into Boolean.features

featureDump = open("Boolean.features", "a+")
pickle.dump(list(set(hamFeatures.keys()).union(set(spamFeatures.keys()))), featureDump) 
featureDump.close()
