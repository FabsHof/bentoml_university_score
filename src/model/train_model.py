import os
from os import path
import logging
import bentoml
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import joblib
logging.basicConfig(level=logging.INFO)

def train_random_forest_model(processed_data_path: str, model_output_path: str, model_name: str, store_to_disk: bool = True) -> None:
    '''
    Train a Random Forest model using processed data and save the trained model.
    Parameters:
    - processed_data_path: str : The file path to the processed data.
    - model_output_path: str : The directory path to save the trained model.
    - model_name: str : The name to use when saving the model to BentoML.
    - store_model: bool : Whether to save the trained model to disk.
    Returns:
    - None
    '''
    X_train_path = path.join(processed_data_path, 'X_train.csv')
    y_train_path = path.join(processed_data_path, 'y_train.csv')
    X_test_path = path.join(processed_data_path, 'X_test.csv')
    y_test_path = path.join(processed_data_path, 'y_test.csv')
    model = RandomForestRegressor(n_estimators=100, n_jobs=-1, criterion='friedman_mse', random_state=42)
 
    if path.exists(X_train_path) and path.exists(y_train_path):
        X_train = pd.read_csv(X_train_path)
        y_train = pd.read_csv(y_train_path).values.ravel()
        model.fit(X_train, y_train)
        # Save model to disk
        if store_to_disk:
            os.makedirs(model_output_path, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_path = path.join(model_output_path, f'{model_name}_{timestamp}.joblib')
            joblib.dump(model, model_path)
            logging.info(f'Model trained and saved to disk: {model_path}.')
        # Save model to BentoML model store
        bentoml.sklearn.save_model(model_name, model)
        logging.info(f'Model trained and saved to BentoML model store as "{model_name}".')
        # Evaluate model
        X_test = pd.read_csv(X_test_path)
        y_test = pd.read_csv(y_test_path).values.ravel()
        rmse = root_mean_squared_error(y_test, model.predict(X_test))
        logging.info(f'Training metrics: RMSE={rmse}')
    else:
        print("Training data not found.")

def main():
    bento_model_name = 'university_admission_rf_model'
    processed_data_path = path.join(os.getcwd(), 'data', 'processed')
    model_output_path = path.join(os.getcwd(), 'models')
    train_random_forest_model(processed_data_path, model_output_path, model_name=bento_model_name, store_to_disk=False)

if __name__ == "__main__":
    main()