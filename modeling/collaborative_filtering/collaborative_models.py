from base_operations import base_operations


class collaborative_models(base_operations):
    def __init__(self, algo_name):
        self.algo_name = algo_name
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

    def train_best_model_generate_ratings_test(self, ratings_set, test_set):
        """
        Train the best model (with minimum AMSE) on the complete ratings set and then compute the ratings for the test set
        :param ratings_set: The complete ratings data set
        :param test_set: The streams for the users for which ratings are not yet available
        :return: A data frame of the form user, stream, predicted rating
        """
        pass
