from collaborative_models import collaborative_models
import constants
import model_params

from surprise import SVD
from surprise import accuracy
from surprise.model_selection import GridSearchCV


class svd_algo_wrapper(collaborative_models):
    """
    The SVD algorithm
    """
    def __init__(self):
        super(svd_algo_wrapper, self).__init__(constants.SVD_ALGO_NAME)

    def evaluate_on_test(self, train_set, test_set):
        """
        Evaluate the algorithm on the test set after running it on the test set
        :param train_set:
        :param test_set:
        :return: RMSE value on test set
        """
        if train_set is not None and test_set is not None:
            print("Evaluate RMSE on test data")
            self.LOG_HANDLE.info("Evaluate RMSE on test data")

            # Use the famous SVD algorithm.
            algo = SVD()

            # Train the algorithm on the trainset, and predict ratings for the testset
            algo.fit(train_set)
            predictions = algo.test(test_set)

            # Then compute RMSE
            return accuracy.rmse(predictions)

    def perform_grid_search_with_cv(self, train_set):
        """
        Perform grid search to get optimal parameters and get metrics after cross validation
        :param train_set: The train set
        :return: Different RMSE and MAE for the different hyper parameters
        """
        if train_set:
            print("Running grid search to find optimal hyper parameters")
            self.LOG_HANDLE.info("Running grid search to find optimal hyper parameters")

            param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005], 'reg_all': [0.4, 0.6]}
            gs = GridSearchCV(SVD, param_grid, measures=model_params.all_models_training_error_measures, cv=model_params.cross_validation_folds)
            gs.fit(train_set)

            # best RMSE score
            print(gs.best_score['rmse'])

            # combination of parameters that gave the best RMSE score
            print(gs.best_params['rmse'])


