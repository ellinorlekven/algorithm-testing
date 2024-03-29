import numpy as np

inputs = [1, 2, 3, 2.5] # can be values or features from a sensor or sample

weights = [[0.2, 0.8, -0.5, 1.0],
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]
biases = [2, 3, 0.5]

# testing the difference in effect betweeen weight and bias
some_value = 0.5
weight = -0.7
bias = 0.7

print(some_value*weight) # weight
print(some_value+bias) # bias

# Calculating the outputs in each node
layer_outputs = []
for neuron_weights, neuron_bias, in zip(weights, biases):
    neuron_output = 0 # output of given neuron
    for n_input, weight in zip(inputs, neuron_weights):
        neuron_output += n_input*weight
    neuron_output += neuron_bias
    layer_outputs.append(neuron_output)
print(layer_outputs)

# using numpy for the same calculation
output = np.dot(weights, inputs) + biases # weights must be first argument (because of indexing)
print(output)
