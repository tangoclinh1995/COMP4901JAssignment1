import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
        that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    
    num_classes = W.shape[1]
    num_train = X.shape[0]
    
    for i in xrange(num_train):
        score = X[i].dot(W)
        correct_class_score = score[y[i]]
        
        # Update loss
        sumExp = np.exp(score).sum()
        
        loss += np.log(sumExp) - correct_class_score
        
        # Update gradient dW
        dW[:, y[i]] -= X[i, :].transpose()
        
        for j in xrange(num_classes):
            dW[:, j] += (1 / sumExp) * np.exp(score[j]) * X[i].transpose()
    
    loss = loss / num_train + reg * np.sum(W * W)
    
    dW = dW / num_train + 2 * reg * W
    
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    
    # Compute loss
    num_classes = W.shape[1]
    num_train = X.shape[0]
    size_data = W.shape[0]
    
    matScore = X.dot(W)
    exampleSumExp = np.exp(X.dot(W)).sum(axis = 1)
    exampleLoss = np.log(exampleSumExp) - matScore[range(num_train), y]
    
    loss = exampleLoss.sum() / num_train + reg * np.sum(W * W)    
    
    # Compute gradient
    matGradContrib = np.zeros((num_train, num_classes, ))
    matGradContrib[range(num_train), y] -= 1
    matGradContrib += np.exp(matScore) * (1 / exampleSumExp).reshape(num_train, 1)
    
    dW = X.transpose().dot(matGradContrib) / num_train + 2 * reg * W    
    
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################

    return loss, dW

