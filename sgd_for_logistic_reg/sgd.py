import string
import math
import numpy
import sys
import random
from matplotlib import pyplot

def zerolog(x):
    # this function is just to monotonically decrease the data points
    # in the integer-valued dataset.
    if x <= 0:
        return 0
    else:
        return math.log(x)

# assume: input data is small enough to fit entirely in memory
def read_input_file(f):
    output_vector = []
    
    for line in f.readlines()[1:]:
        processed = map(float, string.split(line))
        for i in range(1, len(processed)):
            processed[i] = zerolog(processed[i])
            
        output_vector += [processed]

    return output_vector

def predict(observation,weight_vector):
    # Calculate logistic regression
    # h_w(x) = 1/(1+e^-(w*x))

    dp = min(-numpy.dot(observation,weight_vector), 500)

    return 1/float(1+math.exp(dp))

def create_validation_set(examples):
    new_examples = examples
    random.shuffle(new_examples)

    validation_set_size = (len(new_examples)/10)
    
    return (new_examples[:validation_set_size], new_examples[validation_set_size:])

# Stochastic gradient descent

def sgd(f):
    # Read the input file
    examples = read_input_file(f)
    validation_set, training_set = create_validation_set(examples)
    xplot = []
    yplot = []

    # Perform stochastic gradient descent
    # Weight updates performed with the derivative of the log-likelihood
    # ln(L(h | w, x, y)) = (y - h_w(x))x
    # w_i = w_i + \alpha * (y_i - h_w(x_i)) * x_i

    # Initialize weight vector w:
    w = [0] * (len(training_set[0])-1)
    
    # Learning rate should decay with time, but for now we're just leaving it constant.
    learning_rate = 1/float(len(training_set))
    threshold = 0.0001
    old_error = sys.maxint
    d_error = sys.maxint

    iterations = 0
    while d_error > threshold: # While we have not yet "converged"
        # Pick a random example
        ex = random.choice(training_set)

        old_w = list(w)
        for i in range(1, len(ex)):
            # Convert 0/1 to -1/1, since we're encouraging the logistic regression to 
            # grow one way or another with each observation, not zero it out.
            y = 1
            if (ex[0] == 0):
                y = -1
            # for w vector, we want to index at i-1 since len(ex) = len(w) + 1, since we
            # didn't take out the 0/1 classification out of ex (which is the first weight
            # in ex)
            w[i-1] = old_w[i-1] + (learning_rate * ((y - y*predict(ex[1:], old_w)) * ex[i]))

        # Calculate errors
        sumerror = 0
        for item in validation_set:
            sumerror += abs(item[0] - predict(item[1:], w))
        
        d_error = abs(old_error - sumerror)
        old_error = sumerror
        iterations += 1
        print "Iteration " + str(iterations) + " yielded an error of " + str(old_error)
        
        xplot += [iterations]
        yplot += [old_error]

    pyplot.plot(xplot, yplot)
    pyplot.title("Stochastic Gradient Descent Learning Curve (alpha = 1/900, threshold = 0.0001)")
    pyplot.xlabel("Number of Iterations")
    pyplot.ylabel("Sum Error on Validation Set (max error = 100)")
    pyplot.show()

    return w

sgd(open("kredit.asc", "r"))
