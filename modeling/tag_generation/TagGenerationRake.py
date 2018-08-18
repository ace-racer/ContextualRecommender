from rake_nltk import Rake
import configurations
import constants
from base_operations import base_operations
from tag_generation.TagGeneratorBase import TagGeneratorBase

class RakeTagGenerator(TagGeneratorBase):
    def __init__(self):
        print("The RAKE tag generator will be used. " )
        self._rake = Rake()

    def generate_tags(self):
        complete_stream_details_dict = self.get_stream_details()
        stream_id_tag_list = []

        
        for k in complete_stream_details_dict:
            content = complete_stream_details_dict[k]
            content = content.lower()
            self._rake.extract_keywords_from_text(content)

            for item in self._rake.get_ranked_phrases():
                stream_id_tag_list.append((str(k), str(item))) 

        self.create_stream_tag_mapping_file(stream_id_tag_list)
