import numpy as np

theta = np.array([0.0, 0.0, 0.0])
V = np.array([1.06, 1.00, 1.00])

P_spec = np.array([0.0, -0.8, -0.6])
Q_spec = np.array([0.0, -0.4, -0.3])

lines = [
    (0, 1, 0.02, 0.10),
    (0, 2, 0.03, 0.12),
    (1, 2, 0.025, 0.11),
]

Y = np.zeros((3,3), dtype=complex)
for i, j, R, X in lines:
    y = 1/ complex(R, X)
    Y[i, i] += y
    Y[j, j] += y
    Y[i, j] -= y
    Y[j, i] -= y

print('Ybus:\n', Y)