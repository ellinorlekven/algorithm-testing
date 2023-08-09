# We don't have a good way to determine the accuracy/ how wrong the model is
layer_outputs =  [4.8, 1.21, 2.385]
layer_outputs = [4.8, 4.79, 4.25]

#------------------------------------------------------
import math

layer_outputs = [4.8, 1.21, 2.385]

E = math.e

exp_values = []

for output in layer_outputs:
    exp_values.append(E**output)

print(exp_values)

# Coding in the normalizarization
norm_base  = sum(exp_values)
norm_values = []

for value in exp_values:
    norm_values.append(value / norm_base)

print(norm_values)
print(sum(norm_values))