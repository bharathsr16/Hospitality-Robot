import nltk
import os

# Create a .nltk_data directory in the root of the project
nltk_data_dir = os.path.join(os.path.dirname(__file__), ".nltk_data")
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

# Set the NLTK data path
nltk.data.path.append(nltk_data_dir)

# Download the NLTK data
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('punkt_tab', download_dir=nltk_data_dir)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_dir)
nltk.download('maxent_ne_chunker', download_dir=nltk_data_dir)
nltk.download('words', download_dir=nltk_data_dir)
