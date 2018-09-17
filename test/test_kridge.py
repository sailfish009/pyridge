from pyridge.utils import metric_dict
from pyridge.algorithm import algorithm_dict
from pyridge.utils import cross_validation
from pyridge.utils.preprocess import prepare_data

import logging

logger = logging.getLogger('PyRidge')
logger.setLevel(logging.DEBUG)


def test_arrhythmia(train_data=None,
                    train_j_target=None,
                    test_data=None,
                    test_j_target=None):
    """
    Simple test with a UCI database.
    """
    # Data
    if train_data is None or train_j_target is None:
        folder = 'data/arrhythmia'
        train_dataset = 'train_arrhythmia.1'
        train_data, train_j_target = prepare_data(folder=folder,
                                                  dataset=train_dataset)
    if test_data is None or test_j_target is None:
        test_dataset = 'test_arrhythmia.1'
        n_targ = train_j_target.shape[1]
        test_data, test_j_target = prepare_data(folder=folder,
                                                dataset=test_dataset,
                                                n_targ=n_targ)

    # Algorithm
    metric = metric_dict['accuracy']
    algorithm = algorithm_dict['KRidge']
    C_range = [10**i for i in range(-2, 3)]
    k_range = [10**i for i in range(-2, 3)]
    kernel_fun = 'rbf'

    hyperparameters = {'kernelFun': kernel_fun,
                       'C': C_range,
                       'k': k_range}

    clf = algorithm()
    clf.set_cv_range(hyperparameters)
    cross_validation(classifier=clf, train_data=train_data, train_target=train_j_target)
    pred_targ = clf.predict(test_data=test_data)
    acc = metric(pred_targ=pred_targ,
                 real_targ=test_j_target)

    logger.info('Accuracy for algorithm KRidge and dataset arrhythmia.1,'
                ' is {}'.format(acc))


if __name__ == '__main__':
    test_arrhythmia()
