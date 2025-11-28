import os
from os import path
import pandas as pd
import sklearn.model_selection
import logging
logging.basicConfig(level=logging.INFO)

def prepare_data(raw_file: str, processed_path: str) -> None:
    '''
    Prepare raw data by handling missing values and encoding categorical variables.
    Parameters:
    - raw_file: str : The file path to the raw data.
    - processed_path: str : The file path to save the processed data.
    '''
    os.makedirs(path.dirname(processed_path), exist_ok=True)

    df = pd.read_csv(raw_file)

    # Handle missing values
    df.fillna(df.median(), inplace=True)

    # Scale numerical values according to their different scoring scales
    numerical_columns = {'GRE Score': 340, 'TOEFL Score': 120, 'University Rating': 5, 'SOP': 5.0, 'LOR ': 5.0, 'CGPA': 10.0}
    for col, max_value in numerical_columns.items():
        df[col] = df[col] / max_value

    # Train-test split
    train_df, test_df = sklearn.model_selection.train_test_split(df, test_size=0.2, random_state=42)

    X_train = train_df.drop('Chance of Admit ', axis=1)
    y_train = train_df['Chance of Admit ']
    X_test = test_df.drop('Chance of Admit ', axis=1)
    y_test = test_df['Chance of Admit ']
    X_train.to_csv(path.join(processed_path, 'X_train.csv'), index=False)
    y_train.to_csv(path.join(processed_path, 'y_train.csv'), index=False)
    X_test.to_csv(path.join(processed_path, 'X_test.csv'), index=False)
    y_test.to_csv(path.join(processed_path, 'y_test.csv'), index=False)

def main() -> None:
    raw_file = path.join(os.getcwd(), 'data', 'raw', 'admission.csv')
    processed_path = path.join(os.getcwd(), 'data', 'processed')
    prepare_data(raw_file, processed_path)

if __name__ == "__main__":
    main()