import numpy as np
import nnfs

layer_outputs = [[4.8, 1.21, 2.385],
                 [8.9, -1.81, 0.2],
                 [1.41, 1.051, 0.026]]

exp_values = np.exp(layer_outputs)
norm_values = exp_values / np.sum(layer_outputs, axis = 1) # Adding the normalizarization


# Logic: Input -> Exponentiate -> Normalize -> Output
# Softmax = exponentiation + normalization
# Using this logic to make the Softmax Activation

#--------------------- from part 5 ---------------------

from nnfs.datasets import spiral_data

nnfs.init()

# Define the hidden layers
class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons) # gaussian distribution
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


# Make the ReLU activation function
class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis = 1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis = 1, keepdims=True)
        self.output = probabilities

X, y = spiral_data(samples=100, classes=3)

dense1 = Layer_Dense(2,3) # Input must be 2, output can be anything I want
activation1 = Activation_ReLU()

dense2 = Layer_Dense(3, 3) # Input must be dense1's output but can have any number of output
activation2 = Activation_Softmax()

dense1.forward(X)
activation1.forward(dense1.output)

dense2.forward(activation1.output)
activation2.forward(dense2.output)

print(activation2.output[:5])
