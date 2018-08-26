import numpy as np
from numpy.random import seed


class Perceptron(object):
    def __init__(self, eta, iter, shuffle, w=None):
        self.eta = eta
        self.iter = iter
        self.shuffle = shuffle
        self.w_ = w
        self.w_initialized = True
        seed(True)

    def fit(self, x, y):
        if not self.w_initialized:
            self.initialize_w(x.shape[1])
        self.cost_ = []
        for i in range(self.iter):
            if self.shuffle:
                x, y = self.tasuj(x, y)
            cost2 = []
            for xi, target in zip(x, y):
                cost2.append(self.update(xi, target))
            self.cost_.append(sum(cost2) / len(cost2))
        return self

    def initialize_w(self, size):
        self.w_ = np.zeros(1 + size)
        self.w_initialized = True

    def update(self, xi, target):
        output = self.net_input(xi)
        errors = target - output
        self.w_[1:] += self.eta * xi.dot(errors)
        self.w_[0] += self.eta * errors
        return errors**2 / 2

    def tasuj(self, x, y):
        ran = np.random.permutation(len(y))
        return x[ran], y[ran]

    def net_input(self, x):
        return np.dot(x, self.w_[1: ]) + self.w_[0]

    def activation(self, x):
        return self.net_input(x)

    def predict(self, x):
        return np.where(self.activation(x ) >= 0, 1, -1)


