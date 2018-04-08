# custom imports
import constants
import configurations
from data_preparer import data_preparer
from collaborative_filtering_modeller import collaborative_filtering_modeller

def main():
    """
    Executes methods from the modules that need to be run
    :return: None
    """
    if configurations.GENERATE_RATINGS_FILES:
        preparer = data_preparer()
        preparer.perform_operation()

    if configurations.EVALUATE_ALL_MODELS:
        all_modeller = collaborative_filtering_modeller()
        all_modeller.perform_operation()


if __name__ == "__main__":
    main()
    print("Execution completed...")