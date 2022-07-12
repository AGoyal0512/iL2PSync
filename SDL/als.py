import numpy as np

class ALS:
    def __init__(self, X, rank, W_i=None, H_i=None, iter=128, non_negativity_W=False, non_negativity_H=False):
        """Constructor for the ALS object to apply various modifications of the Alternating Least Squares algorithm on.
        We want to compute W and H such that we are able to minimize || X - WH ||_{F}^2

        Args:
            X (2D-ndarray): The original m by n matrix that you wish to factorize
            rank (int): The number of columns in the computed dictionary
            W_i (2D-ndarray, optional): The initialized value of the dictionary matrix. Defaults to None.
            H_i (2D-ndarray, optional): The initialized value of the encoding matrix. Defaults to None.
            iter (int, optional):Number of iterations to run the ALS for. Defaults to 128.
            non_negativity_W (bool, optional): Specify whether we want non-negativity constraints on computed W. Defaults to False.
            non_negativity_H (bool, optional): Specify whether we want non-negativity constraints on computed H. Defaults to False.
        """
        self.X = X

        self.W_i = W_i
        if self.W_i is None:
            self.W_i = np.random.rand(np.shape(self.X)[0], self.rank)

        self.H_i = H_i
        if self.H_i is None:
            self.H_i = np.random.rand(self.rank, np.shape(self.X)[1])
        

        self.rank = rank
        self.iter = iter
        self.non_negativity_W = non_negativity_W
        self.non_negativity_H = non_negativity_H
    
    def fit(self):
        """Applies the classical ALS with the L2-norm (Frobenius norm) on the created ALS object

        Returns:
            W (2D-ndarray): The final value of the dictionary matrix.
            H (2D-ndarray): The final value of the encoding matrix.
        """
        for i in range(self.iter):
            self.H_i = np.linalg.lstsq(self.W_i, self.X, rcond=None)[0]
            if self.non_negativity_H:
                self.H_i[self.H_i < 0] = 0

            self.W_i = np.transpose(np.linalg.lstsq(np.transpose(self.H_i), np.transpose(self.X), rcond=None)[0])
            if self.non_negativity_W:
                self.W_i[self.W_i < 0] = 0

        W, H = self.W_i, self.H_i
        return W, H
