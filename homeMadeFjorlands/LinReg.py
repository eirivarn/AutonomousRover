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

/CODE/grpc $ ldd /usr/local/lib/python3.9/dist-packages/grpc/_cython/cygrpc.cpython-39-arm-linux-gnueabihf.so
        linux-vdso.so.1 (0xbeef7000)
        /usr/lib/arm-linux-gnueabihf/libarmmem-${PLATFORM}.so => /usr/lib/arm-linux-gnueabihf/libarmmem-v7l.so (0xb698b000)
        libpthread.so.0 => /lib/arm-linux-gnueabihf/libpthread.so.0 (0xb695f000)
        libatomic.so.1 => /lib/arm-linux-gnueabihf/libatomic.so.1 (0xb6946000)
        libstdc++.so.6 => /lib/arm-linux-gnueabihf/libstdc++.so.6 (0xb67be000)
        libm.so.6 => /lib/arm-linux-gnueabihf/libm.so.6 (0xb674f000)
        libc.so.6 => /lib/arm-linux-gnueabihf/libc.so.6 (0xb65fb000)
        /lib/ld-linux-armhf.so.3 (0xb6fcc000)
        libgcc_s.so.1 => /lib/arm-linux-gnueabihf/libgcc_s.so.1 (0xb65ce000)