import numpy as np


class Perceptron(object):
    def __init__(self, eta, iter):
        self.eta = eta
        self.iter = iter

    def fit(self, x, y):
        self.w_ = np.zeros(x.shape[1] + 1)
        self.cost_ = []
        for i in range(self.iter):
            output = self.net_input(x)
            errors = (y - output)

            self.w_[1:] += self.eta * x.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum() / 2
            self.cost_.append(cost)
        return self

    def net_input(self, x):
        return np.dot(x, self.w_[1: ]) + self.w_[0]

    def activation(self, x):
        return self.net_input(x)

    def predict(self, x):
        return np.where(self.activation(x ) >= 0, 1, -1)


