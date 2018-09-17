# custom imports
import constants
import configurations
from collaborative_filtering.data_preparer import data_preparer
from collaborative_filtering.collaborative_filtering_modeller import collaborative_filtering_modeller
import argparse
from collaborative_filtering.best_model_output_generator import best_model_output_generator
from stream_similarity.stream_tag_one_hot_encoder import stream_tag_one_hot_encoder
from stream_similarity.stream_similarity_evaluator import stream_similarity_evaluator
from tag_generation.TagGeneratorBase import TagGeneratorBase

def main():
    """
    Executes methods from the modules that need to be run
    :return: None
    """

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-tags', type=int, help='Whether to generate the tags from the complete stream details.', required=False)
    arg_parser.add_argument('-tf', type=int, help='Whether to generate the tag frequencies for the streams. Enter a value of 1, if you want files to be generated and 0 otherwise.', required=False)
    arg_parser.add_argument('-d', type=str, help='The distance metric to use to compute the similar streams. Accepted values = {0},{1} and {2}'.format(constants.JACCARD_SIMILARITY, constants.CUSTOM_DISTANCE, constants.COSINE_SIMILARITY), required=False)
    arg_parser.add_argument('-g', type=int, help='Whether to generate the ratings files (for collaborative filtering). Enter a value of 1, if you want files to be generated and 0 otherwise.', required=False)
    arg_parser.add_argument('-e', type=int, help='Evaluate all recommender models (for collaborative filtering). Enter a value of 1, if you want all recommender systems to be evaluated and 0 otherwise.', required=False)
    arg_parser.add_argument('-gp', type=int, help='Generate predictions for a user using the best collaborative filtering algorithm. Enter a value of 1, if you want the file to be generated and 0 otherwise.', required=False)
    arg_parser.add_argument('-all', type=int, help='Whether all options should be executed. If set to 1 will override all other values.', required=False)
    arg_parser.add_argument('-content_all', type=int, help='Whether all options for content filtering should be executed. If set to 1 will override all other values.', required=False)
    args = arg_parser.parse_args()
    
    should_all_content_filtering_be_executed = (args.content_all == 1)
    should_all_options_be_executed = (args.all == 1)
    if should_all_options_be_executed:
        should_generate_ratings_file = True
        should_evaluate_models = True
        should_generate_tag_frequencies = True
        similar_streams_distance_metric = constants.COSINE_SIMILARITY
        should_generate_predicted_streams_for_user = True
        should_tags_be_generated = True
    elif should_all_content_filtering_be_executed:
        should_tags_be_generated = True
        should_generate_tag_frequencies = True
        similar_streams_distance_metric = constants.COSINE_SIMILARITY
        should_generate_ratings_file = False
        should_evaluate_models = False
        should_generate_predicted_streams_for_user = False
    else:
        should_generate_ratings_file = (args.g == 1)
        should_evaluate_models = (args.e == 1)
        should_generate_tag_frequencies = (args.tf == 1)
        similar_streams_distance_metric = args.d
        should_generate_predicted_streams_for_user = (args.gp == 1)
        should_tags_be_generated = (args.tags == 1)

    if should_tags_be_generated:
        print("Tags will be generated from the complete stream details")
        tag_generator = configurations.TAG_GENERATION_ALGORITHM()
        tag_generator.generate_tags()
    
    if should_generate_tag_frequencies:
        print("Will generate the tag frequencies...")
        stream_tag_encoder = stream_tag_one_hot_encoder()
        stream_tag_encoder.perform_operation()

    if similar_streams_distance_metric:
        print("Computing similar streams")
        similar_streams_evaluator = stream_similarity_evaluator(similar_streams_distance_metric)
        similar_streams_evaluator.perform_operation()
    
    # Collaborative filtering implementation starts
    if should_generate_ratings_file:
        print("Will generate the ratings files...")
        preparer = data_preparer()
        preparer.perform_operation()

    if should_evaluate_models:
        print("Will evaluate all recommender models...")
        all_modeller = collaborative_filtering_modeller()
        all_modeller.perform_operation()
    
    if should_generate_predicted_streams_for_user:
        print("Will run the best model to generate predicted ratings")
        best_model_train_executor = best_model_output_generator()
        best_model_train_executor.perform_operation()


if __name__ == "__main__":
    print("Execution started...")
    main()
    print("Execution completed...")