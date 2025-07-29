import pandas as pd
from sklearn.model_selection import train_test_split
import os
import yaml 

import logging

# configure logging
logger = logging.getLogger('data_ingestion')
logger.setLevel('DEBUG')


#console handler
console_handler=logging.StreamHandler()
console_handler.setLevel('DEBUG')

#file handler
file_handler=logging.FileHandler('error.log')
file_handler.setLevel('ERROR')

formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)



def load_params(params_path: str) -> float:
       try:
              with open(params_path,'r') as file:
                     params=yaml.safe_load(file)
              test_size=params['data_ingestion']['test_size']
              logger.debug('Test size retrived')
              return test_size
       except FileNotFoundError:
              logger.error(f"The file {params_path} was not found.")
              raise
       except yaml.YAMLObject as e:
              logger.error(f"Failed to parse the yaml file {params_path}.")
              raise
       except Exception as e:
              logger.error(f"An unexpected error caused while loading YAML file.")
              raise

       
def read_data(url: str) -> pd.DataFrame:
       try:
              df = pd.read_csv(url)
              return df
       except pd.errors.ParserError as e:
              print(f'Failed to parse csv file from the url {url}.')
              print (e)
              raise
       except Exception as e:
              print(f"An unexpected error caused while loading the data.")
              print(e)
              raise


def process_data(df: pd.DataFrame) ->pd.DataFrame:
       try:
              df.drop(columns='tweet_id', inplace=True)
              df['sentiment'].replace({'empty':2, 'sadness':0, 'enthusiasm':3, 'neutral':4, 'worry':5, 'surprise':6,
              'love':7, 'fun':8, 'hate':9, 'happiness':1, 'boredom':10, 'relief':11, 'anger':12}, inplace=True)
              return df
       except KeyError as e:
              print(f"Missing coloumn {e} in Dataframe.")
              raise
       except Exception as e:
              print(f"An unexpected error occured while preprocessing")
              print(e)
              raise

       
       
def save_data(data_path: str,train_data: pd.DataFrame,test_data: pd.DataFrame) ->None:
       try:
              os.makedirs(data_path,exist_ok=True)
              train_path = os.path.join(data_path, 'train.csv')
              test_path = os.path.join(data_path, 'test.csv')

              train_data.to_csv(train_path, index=False)
              test_data.to_csv(test_path, index=False)

              print(f"Data saved successfully to {data_path}")
       except OSError as os_err:
        print(f"Directory creation or file saving failed: {os_err}")
        print (os_err)
        raise

       except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print (e)
        raise


##creatte a main function to call all the function
def main():
       try:
              test_size= load_params('params.yaml')
              df= read_data('https://raw.githubusercontent.com/campusx-official/jupyter-masterclass/main/tweet_emotions.csv')
              df=process_data(df)
              #train test split
              train_data, test_data = train_test_split(df, test_size=test_size, random_state=42)
               #step 2 :create local copy
              data_path=os.path.join("data",'raw')
              save_data(data_path,train_data,test_data)
       except Exception as e:
             print(f'Failed to complete the data ingestion process.')
             print (e)
             raise

if __name__== "__main__":
       main()
















#now we can go ahead and create pipeline for this .We will have to code in 
#yaml file which can be generted by DVC
# dvc stage add -n (name of stage) -d (src/data_ingestion.py) -p (parameters) -o (data/raw) 

# to run dvc stage add -n (name of stage) -d (src/data_ingestion.py) -p (parameters) -o (data/raw) python src/data_ingestion.py

# -n (name of folder)
# -d(dependency of file)
# -p (parameters)
# -o(output)


# to run the pipe line- dvc repro

# to vizualize pipeline -- dvc dag

