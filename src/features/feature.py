import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
import yaml
import logging

# logging configuration
logger = logging.getLogger('feature_engineering')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

file_handler = logging.FileHandler('feature_engineering_errors.log')
file_handler.setLevel('ERROR')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_param(params_path:str) ->dict:
    "load parameter from YAML file"
    try:
        with open (params_path,'r') as file:
            params=yaml.safe_load(file)
            logger.debug('Parameters retrieved from %s', params_path)
            return params
    
    except FileNotFoundError:
        logger.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logger.error('YAML error: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error: %s', e)
        raise

def load_data(file_path:str)-> pd.DataFrame:
    """load data from csv file"""
    try:
        df=pd.read_csv(file_path)
        df.fillna('', inplace=True)
        logger.debug('Data loaded and NaNs filled from %s', file_path)
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the data: %s', e)
        raise

def apply_bow(train_data: pd.DataFrame, test_data: pd.DataFrame, max_features: int) -> tuple:
    """Apply BOW to the data."""
    try:
        vectorizer = CountVectorizer(max_features=max_features)
        X_train = train_data['content'].values
        y_train = train_data['sentiment'].values
        X_test = test_data['content'].values
        y_test = test_data['sentiment'].values
        # Fit the vectorizer on the training data and transform it
        X_train_bow = vectorizer.fit_transform(X_train)
        # Transform the test data using the same vectorizer
        X_test_bow = vectorizer.transform(X_test)
        #regroup the data frame
        train_df = pd.DataFrame(X_train_bow.toarray())
        train_df['label'] = y_train
        test_df = pd.DataFrame(X_test_bow.toarray())
        test_df['label'] = y_test
        logger.debug('Bag of Words applied and data transformed')
        return train_df,test_df
    
    except Exception as e:
        logger.error('Error during Bag of Words transformation: %s', e)
        raise

def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save the dataframe to a CSV file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.debug('Data saved to %s', file_path)
    except Exception as e:
        logger.error('Unexpected error occurred while saving the data: %s', e)
        raise

def main():
    try:
        params=load_param('params.yaml')
        max_feature=params['feature']['max_features']

        train_data = load_data('./data/interim/train_processed.csv')
        test_data = load_data('./data/interim/test_processed.csv')

        train_df,test_df=apply_bow(train_data,test_data,max_feature)

        save_data(train_df,os.path.join("./data", "processed", "train_bow.csv"))
        save_data(test_df,os.path.join("./data", "processed", "test_bow.csv"))
    except Exception as e:
        logger.error('Failed to complete the feature engineering process: %s', e)
        print(f"Error: {e}")

if __name__== "__main__":
       main()

    


    























