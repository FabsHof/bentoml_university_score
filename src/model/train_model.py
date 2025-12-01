import os
from os import path
import logging
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import joblib
logging.basicConfig(level=logging.INFO)

def train_random_forest_model(processed_data_path: str, model_output_path: str, store_model: bool = True) -> None:
    '''
    Train a Random Forest model using processed data and save the trained model.
    Parameters:
    - processed_data_path: str : The file path to the processed data.
    - model_output_path: str : The directory path to save the trained model.
    - store_model: bool : Whether to save the trained model to disk.
    Returns:
    - None
    '''
    X_train_path = path.join(processed_data_path, 'X_train.csv')
    y_train_path = path.join(processed_data_path, 'y_train.csv')
    X_test_path = path.join(processed_data_path, 'X_test.csv')
    y_test_path = path.join(processed_data_path, 'y_test.csv')
    model = RandomForestRegressor(n_estimators=100, criterion='friedman_mse', n_jobs=-1, random_state=42)
 
    if path.exists(X_train_path) and path.exists(y_train_path):
        X_train = pd.read_csv(X_train_path)
        y_train = pd.read_csv(y_train_path).values.ravel()
        model.fit(X_train, y_train)
        if store_model:
            os.makedirs(model_output_path, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_path = path.join(model_output_path, f'{timestamp}_random_forest_model.joblib')
            joblib.dump(model, model_path)
            logging.info(f'Model trained and saved to {model_path}.')
        X_test = pd.read_csv(X_test_path)
        y_test = pd.read_csv(y_test_path).values.ravel()
        rmse = root_mean_squared_error(y_test, model.predict(X_test))
        logging.info(f'Training metrics: RMSE={rmse}')
    else:
        print("Training data not found.")

def main():
    processed_data_path = path.join(os.getcwd(), 'data', 'processed')
    model_output_path = path.join(os.getcwd(), 'models')
    train_random_forest_model(processed_data_path, model_output_path)

if __name__ == "__main__":
    main()