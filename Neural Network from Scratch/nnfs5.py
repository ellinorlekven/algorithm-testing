import numpy as np
import nnfs
from nnfs.datasets import spiral_data

nnfs.init()

# Input
X = [[1, 2, 3, 2.5],
     [2.0, 5.0, -1.0, 2.0],
     [-1.5, 2.7, 3.3, -0.8]]

# Make data (described by two unique features)
X, y = spiral_data(100, 3)

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


layer1 = Layer_Dense(2,5) # The n_neurons must be the n_inputs (in this case: two)
layer1.forward(X)
print(layer1.output)

# Remove all the negative values and turn them into zeros
activation1 = Activation_ReLU()
activation1.forward(layer1.output)
print(activation1.output)
