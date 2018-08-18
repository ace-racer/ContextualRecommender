from rake_nltk import Rake
import configurations
import constants
from base_operations import base_operations
from tag_generation.TagGeneratorBase import TagGeneratorBase

# Uses stopwords for english from NLTK, and all puntuation characters by
# default


# myText = '''The Great Pyramid of Giza (also known as the Pyramid of Khufu or the Pyramid of Cheops) is the oldest and largest of the three pyramids in the Giza pyramid complex bordering what is now El Giza, Egypt. It is the oldest of the Seven Wonders of the Ancient World, and the only one to remain largely intact.

# Based on a mark in an interior chamber naming the work gang and a reference to the fourth dynasty Egyptian Pharaoh Khufu, Egyptologists believe that the pyramid was built as a tomb over a 10- to 20-year period concluding around 2560 BC. Initially at 146.5 metres (481 feet), the Great Pyramid was the tallest man-made structure in the world for more than 3,800 years. Originally, the Great Pyramid was covered by limestone casing stones that formed a smooth outer surface; what is seen today is the underlying core structure. Some of the casing stones that once covered the structure can still be seen around the base. There have been varying scientific and alternative theories about the Great Pyramid's construction techniques. Most accepted construction hypotheses are based on the idea that it was built by moving huge stones from a quarry and dragging and lifting them into place.
# # Extraction given the text.'''

# r.extract_keywords_from_text(myText)

# print "\n"
# # To get keyword phrases ranked highest to lowest.
# print r.get_ranked_phrases()
# print "\n"
# # To get keyword phrases ranked highest to lowest with scores.
# print r.get_ranked_phrases_with_scores()

# print r.get_word_frequency_distribution()

# print r.get_word_degrees()

# print r._generate_phrases(myText)

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
