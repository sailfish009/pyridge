from pyridge.experiment.check import check_algorithm


def test_diverse_elm():
    hyperparameter_div = {'activation': ['sigmoid'],
                          'reg': [10 ** i for i in range(-1, 2)],
                          'div': [10 ** i for i in range(-1, 2)],
                          'hidden_neurons': [10],
                          'size': [5]}
    value_dict = check_algorithm(folder='data',
                                 dataset='iris',
                                 algorithm='DiverseELM',
                                 hyperparameter=hyperparameter_div,
                                 metric_list=['accuracy', 'rmse', 'diversity'])


def test_diverse_elm_regression():
    hyperparameter_div = {'activation': ['sigmoid'],
                          'reg': [10 ** i for i in range(-1, 2)],
                          'div': [10 ** i for i in range(-1, 2)],
                          'hidden_neurons': [10],
                          'size': [5]}
    value_dict = check_algorithm(folder='data_regression',
                                 dataset='housing',
                                 algorithm='DiverseELM',
                                 hyperparameter=hyperparameter_div,
                                 metric_list=['rmse', 'diversity'],
                                 classification=False)
