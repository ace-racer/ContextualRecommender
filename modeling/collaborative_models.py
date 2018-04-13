from base_operations import base_operations


class collaborative_models(base_operations):
    def __init__(self, algo_name):
        super(collaborative_models, self).__init__(algo_name)

    def evaluate_on_test(self, train_set, test_set):
        """
        Evaluate the algorithm on the test set after running it on the test set
        :param train_set:
        :param test_set:
        :return: RMSE value on test set
        """
        pass

    def perform_grid_search_with_cv(self, train_set):
        """
        Perform grid search to get optimal parameters and get metrics after cross validation
        :param train_set: The train set
        :return: Different RMSE and MAE for the different hyper parameters
        """
        pass
