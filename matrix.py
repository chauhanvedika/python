import numpy as np

# Create two matrices
matrix1 = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

matrix2 = np.array([
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
])

# Addition of two matrices
sum_matrix = matrix1 + matrix2
print("Matrix Sum:")
print(sum_matrix)

# Subtraction of two matrices
difference_matrix = matrix1 - matrix2
print("\nMatrix Difference:")
print(difference_matrix)

# Element-wise multiplication of two matrices
product_matrix = matrix1 * matrix2
print("\nMatrix Element-wise Product:")
print(product_matrix)

# Matrix multiplication (dot product)
dot_product_matrix = np.dot(matrix1, matrix2)
print("\nMatrix Dot Product:")
print(dot_product_matrix)
