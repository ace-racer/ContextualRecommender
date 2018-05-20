all_models_training_error_measures = ['RMSE', 'MAE']
cross_validation_folds = 5
test_set_size = 0.2
svd_best_params = {'n_epochs': 10, 'lr_all': 0.005, 'reg_all': 0.4}
svdpp_best_params = {'n_epochs': 30, 'lr_all': 0.008, 'reg_all': 0.03}
knn_means_best_params = {'k': 30, 'sim_options': {'name': 'msd', 'user_based': False}}