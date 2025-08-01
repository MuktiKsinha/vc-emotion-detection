import numpy as np
import pandas as pd
import os
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import logging


#Logging configrations
logger = logging.getLogger('data_transformation')
logger.setLevel('DEBUG')
console_handler=logging.StreamHandler()
console_handler.setLevel('DEBUG')
file_handler=logging.FileHandler('error.log')
file_handler.setLevel('ERROR')
formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)



#transform the data

nltk.download('wordnet')
nltk.download('stopwords')

def lemmatization(text):
    """Lemmatize the word"""
    lemmatizer= WordNetLemmatizer()
    text = text.split()
    text=[lemmatizer.lemmatize(y) for y in text]
    return " " .join(text)

def remove_stop_words(text):
    """Remove stop words"""
    stop_words = set(stopwords.words("english"))
    Text=[words for words in str(text).split() if words not in stop_words]
    return " ".join(Text)

def removing_numbers(text):
    """remove numbers from text"""
    text=''.join([char for char in text if not char.isdigit()])
    return text

def lower_case(text):
    """convert text to lower case"""
    text = text.split()
    text=[y.lower() for y in text]
    return " " .join(text)

def removing_punctuations(text):
     """Remove punctuations from the text."""
     text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
     text = text.replace('؛', "")
     text = re.sub('\s+', ' ', text).strip()
     return text

def removing_urls(text):
    """remove url from text"""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_small_sentences(df):
    """remove sentence with less than 3 words"""
    for i in range(len(df)):
        if len(df.text.iloc[i].split()) < 3:
            df.text.iloc[i] = np.nan

def normalize_text(df):
    """Normalize the text"""
    try:
       df['content'] = df['content'].apply(lower_case)
       logger.debug('converted to lower case')
       df['content'] = df['content'].apply(remove_stop_words)
       logger.debug('stop words removed')
       df['content'] = df['content'].apply(removing_numbers)
       logger.debug('numbers removed')
       df['content'] = df['content'].apply(removing_punctuations)
       logger.debug('punctuations removed')
       df['content'] = df['content'].apply(removing_urls)
       logger.debug('urls Removed')
       df['content'] = df['content'].apply(lemmatization)
       logger.debug('lemmatization performed')
       logger.debug('Text normalization completed')
       return df

    except Exception as e:
         logger.error('Error during text normalization: %s', e)
         raise


def main():
    try:
        train_data=pd.read_csv('./data/raw/train.csv')
        test_data=pd.read_csv('./data/raw/test.csv')
        logger.debug('Data loaded Successfully')

        train_processed_data = normalize_text(train_data)
        test_processed_data = normalize_text(test_data)

    #store the datainside data/processed or interim

        data_path=os.path.join('data','interim')
        os.makedirs(data_path,exist_ok=True)

    #store train and test data in csv
        train_processed_data.to_csv(os.path.join(data_path,'train_processed.csv'),index=False)
        test_processed_data.to_csv(os.path.join(data_path,'test_processed.csv'),index=False)

        logger.debug('Processed data saved to %s', data_path)

    except Exception as e:
        logger.error('Failed to complete the data transformation process: %s', e)
        print(f"Error: {e}")

if __name__== "__main__":
       main()






#add this stage to dvc yaml file

#dvc stage add -n data_preprocessing -d src/data_preprocessing.py -d data/raw -o data/processed python src/data_preprocessing.py

