from pyelm import logger_pyelm
from pyelm.utils.target_encode import *
from pyelm.generic import KernelMethod


class KELM(KernelMethod):
    """
    Kernel Extreme Learning Machine. Kernel version of the Extreme Learning Machine,
    in which a tranformation from input features space into "hidden layer" is made
    by a kernel trick.
    """
    def __init__(self, parameters=None):
        """
        :type parameters: dict
        :param parameters: dictionary with the parameters needed for training. It must contain:

                - k: length scale of Radial Basis Function kernel
                - C: regularization.

                If None, parameters should be introduced later.
        """
        if parameters is not None:
            self.__call__(parameters)
        logger_pyelm.debug('Kernel Extreme Learning Machine instanced')

    def fit(self, train_data, train_target):
        self.t = train_target.shape[1]
        n = train_data.shape[0]
        m = train_data.shape[1]
        self.train_data = train_data

        omega_train = self.kernel_fun(X=self.train_data)

        if self.C == 0:  # No regularization
            self.output_weight = np.linalg.solve(omega_train, train_target)
        else:
            # alpha = np.eye(H.shape[0]) / self.C + np.dot(H, H.transpose())
            # self.output_weight = np.dot(H.transpose(), np.linalg.solve(alpha, train_target))
            alpha = omega_train + np.eye(n) / self.C
            self.output_weight = np.linalg.solve(alpha, train_target)

    def predict(self, test_data):
        """
        Once instanced, classifier can predict test target from test data, using some mathematical
        rules.

        :param numpy.array test_data: matrix of data to predict.
        :return: matrix of the predicted targets.
        """
        omega_test = self.kernel_fun(X=self.train_data, Y=test_data)
        indicator = np.dot(omega_test.T, self.output_weight)
        test_target = j_renorm(indicator)
        return test_target

    def save_clf_param(self):
        return {'C': self.C,
                'k': self.k,
                'kernel_fun': self.kernel_fun}

    def __call__(self, parameters):
        """
        :type parameters: dict
        :param parameters: dictionary with the parameters needed for training. It must contain:

                - k: length scale of Radial Basis Function kernel
                - C: regularization.
        """
        self.C = parameters['C']
        self.k = parameters['k']  # TODO: it should be more generalized
        self.kernel_fun = self.kernel(length_scale=self.k)
