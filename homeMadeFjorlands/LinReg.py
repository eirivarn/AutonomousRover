import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression

class LinearRegression:
    def fit(self, X, y, method, learning_rate=0.01, iterations=500, batch_size=32):
        X = np.concatenate([X, np.ones_like(y)], axis=1)
        rows, cols = X.shape
        if method == 'solve':
            if rows >= cols == np.linalg.matrix_rank(X):
                self.weights = np.matmul(
                    np.matmul(
                        np.linalg.inv(
                            np.matmul(
                                X.transpose(),
                                X)),
                        X.transpose()),
                    y)
            else:
                print('X has not full column rank. method=\'solve\' cannot be used.')
        elif method == 'sgd':
            self.weights = np.random.normal(scale=1/cols, size=(cols, 1))
            for i in range(iterations):
                Xy = np.concatenate([X, y], axis=1)
                np.random.shuffle(Xy)
                X, y = Xy[:, :-1], Xy[:, -1:]
                for j in range(int(np.ceil(rows/batch_size))):
                    start, end = batch_size*j, np.min([batch_size*(j+1), rows])
                    Xb, yb = X[start:end], y[start:end]
                    gradient = 2*np.matmul(
                        Xb.transpose(),
                        (np.matmul(Xb,
                                   self.weights)
                         - yb))
                    self.weights -= learning_rate*gradient
        else:
            print(f'Unknown method: \'{method}\'')
        
        return self
    
    def predict(self, X):
        if not hasattr(self, 'weights'):
            print('Cannot predict. You should call the .fit() method first.')
            return
        
        X = np.concatenate([X, np.ones((X.shape[0], 1))], axis=1)
        
        if X.shape[1] != self.weights.shape[0]:
            print(f'Shapes do not match. {X.shape[1]} != {self.weights.shape[0]}')
            return
        
        return np.matmul(X, self.weights)
    
    def rmse(self, X, y):
        y_hat = self.predict(X)
        
        if y_hat is None:
            return
        
        return np.sqrt(((y_hat - y)**2).mean())