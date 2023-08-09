import numpy as np

# Example classes:
# 0 - dog
# 1 - cat
# 2 - human


# Example values from an output layer using softmax
softmax_output = np.array([[0.7, 0.1, 0.2],
                           [0.5, 0.1, 0.4],
                           [0.02, 0.9, 0.08]])

class_targets = [0, 1, 1] # The inputs/correct answers could be dog, cat, cat

print(softmax_output[range(len(softmax_output)), class_targets])
neg_log = -np.log(softmax_output[range(len(softmax_output)), class_targets]) # Gets the losses
average_loss = np.mean(neg_log) # Gets the average loss for the model

# Problem:
print(-np.log(0)) # Gives an infinite number
print(np.mean(-np.log(0))) # The mean of infinite = Game Over

# Solution: 
print(-np.log(1-1e-7))

#--------------------- from part 7 ---------------------
import numpy as np
import nnfs
from nnfs.datasets import spiral_data
nnfs.init()

sample = 3
# y_true = [0, 1, 1] # The correct answers


# Define the hidden layers
class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.010 * np.random.randn(n_inputs, n_neurons) # gaussian distribution
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


# Make the ReLU activation function
class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

# Using 'Softmax = exponentiation + normalization'-logic to make the Softmax Activation
class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis = 1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis = 1, keepdims=True)
        self.output = probabilities

# Added in step 8
class Loss:
    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses) # or batch_loss
        return data_loss

class Loss_CategoricalCrossentropy(Loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7)

        if len(y_true.shape) == 1: # Scalar values
            correct_confidences = y_pred_clipped[range(samples), y_true]

        elif len(y_true.shape) == 2: # Onehot encoded vectors
            correct_confidences = np.sum(y_pred_clipped*y_true, axis=1)

        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods


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

# Define loss function, how wrong is the answer?
loss_function = Loss_CategoricalCrossentropy()
loss = loss_function.calculate(activation2.output, y)

print('Loss:', loss)

# Define accuracy function:
predictions = np.argmax(softmax_output, axis=1)
print(predictions)
accuracy = np.mean(predictions == class_targets)
print('Accuracy:', accuracy)
