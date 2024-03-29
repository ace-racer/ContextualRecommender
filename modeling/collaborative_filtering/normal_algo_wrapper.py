from collaborative_filtering.collaborative_models import collaborative_models
import constants
import model_params

from surprise import NormalPredictor
from surprise import accuracy
from surprise.model_selection import GridSearchCV


class normal_algo_wrapper(collaborative_models):
    """
    The SVD algorithm
    """
    def __init__(self):
        super(normal_algo_wrapper, self).__init__(constants.NORMAL_ALGO_NAME)

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

            algo = NormalPredictor()

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
        pass
    
    def train_best_model_generate_ratings_test(self, ratings_set, test_set):
        """
        Train the best model (with minimum RMSE) on the complete ratings set and then compute the ratings for the test set
        :param ratings_set: The complete ratings data set
        :param test_set: The streams for the users for which ratings are not yet available
        :return: A data frame of the form user, stream, predicted rating
        """
        if ratings_set and test_set:
            print("Training the best model and generating the ratings for the test data set")
            self.LOG_HANDLE.info("Training the best model and generating the ratings for the test data set")

            algo = NormalPredictor()
            algo.fit(ratings_set)

            predictions = algo.test(test_set)
            return predictions

