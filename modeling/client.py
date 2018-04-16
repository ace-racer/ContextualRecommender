# custom imports
import constants
import configurations
from data_preparer import data_preparer
from collaborative_filtering_modeller import collaborative_filtering_modeller
import argparse
from best_model_output_generator import best_model_output_generator
from stream_tag_one_hot_encoder import stream_tag_one_hot_encoder


def main():
    """
    Executes methods from the modules that need to be run
    :return: None
    """
    should_generate_ratings_file = configurations.GENERATE_RATINGS_FILES
    should_evaluate_models = configurations.EVALUATE_ALL_MODELS

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-sg', type=int, help='Whether to generate the tag frequencies for the streams.', required=False)
    arg_parser.add_argument('-g', type=int, help='Whether to generate the ratings files.', required=False)
    arg_parser.add_argument('-e', type=int, help='Evaluate all recommender models.', required=False)
    args = arg_parser.parse_args()

    should_generate_ratings_file = (args.g == 1)
    should_evaluate_models = (args.e == 1)
    should_generate_tag_frequencies = (args.sg == 1)

    if should_generate_tag_frequencies:
        print("Will generate the tag frequencies...")
        stream_tag_encoder = stream_tag_one_hot_encoder()
        stream_tag_encoder.perform_operation()

    if should_generate_ratings_file:
        print("Will generate the ratings files...")
        preparer = data_preparer()
        preparer.perform_operation()

    if should_evaluate_models:
        print("Will evaluate all recommender models...")
        all_modeller = collaborative_filtering_modeller()
        all_modeller.perform_operation()

    print("Will run the best model to generate predicted ratings")
    best_model_train_executor = best_model_output_generator()
    best_model_train_executor.perform_operation()


if __name__ == "__main__":
    print("Execution started...")
    main()
    print("Execution completed...")