import pandas as pd
import os
import json

from ml.data_inputer import DataInputer
from ml.knn_data_processor import KNNDataProcessor
from ml.prediction_evaluator import PredictionEvaluator

from ml.ds2.ds2_pre_processor import DS2PreProcessor
from ml.ds2.ds2_xgboost_predictor import DS2XGBoostPredictor

from ml.ds4.ds4_pre_processor import DS4PreProcessor
from ml.ds4.ds4_naive_bayes_predictor import DS4NaiveBayesPredictor
from ml.ds4.ds4_svm_predictor import DS4SVMPredictor

evaluator = PredictionEvaluator()

def ds4(common_columns, query_ds4):
    df4 = pd.read_csv(os.path.join('ml/datasets', 'dataset4.csv'))
    ds4_preprocessor = DS4PreProcessor(df4)
    df4 = ds4_preprocessor.preprocessed_df4
    df4.name = 'ds4'
    
    knn_data_processor_ds4 = KNNDataProcessor(common_columns, df4)
    user_input_processed_df4 = knn_data_processor_ds4.prepare_user_input_for_knn(query_ds4, "ds4")
    nearest_neighbor_row_ds4 = knn_data_processor_ds4.find_nearest_neighbor(user_input_processed_df4)
    
    predictor = DS4NaiveBayesPredictor(df4)
    path = os.path.join('ml/models', 'DS4NaiveBayesPredictor.pkl')
    if not os.path.exists(path):
        predictor.train_model(path)

    prediction = predictor.predict(nearest_neighbor_row_ds4, path)
    evaluator.add_prediction(prediction, weight=0.2)

    predictor = DS4SVMPredictor(df4)
    path = os.path.join('ml/models', 'DS4SVMPredictor.pkl')
    if not os.path.exists(path):
        predictor.train_model(path)

    prediction = predictor.predict(nearest_neighbor_row_ds4, path)
    evaluator.add_prediction(prediction, weight=0.5)

def ds2(common_columns, query_ds2):
    df2 = pd.read_csv(os.path.join('ml/datasets', 'dataset2.csv'))
    ds2_preprocessor = DS2PreProcessor(df2)
    df2 = ds2_preprocessor.preprocessed_df2
    df2.name = 'ds2'

    knn_data_processor_ds2 = KNNDataProcessor(common_columns, df2)
    user_input_processed_df2 = knn_data_processor_ds2.prepare_user_input_for_knn(query_ds2, "ds2")
    nearest_neighbor_row_ds2 = knn_data_processor_ds2.find_nearest_neighbor(user_input_processed_df2)

    ds2_xgb_predictor = DS2XGBoostPredictor(df2)
    
    path = os.path.join('ml/models', 'DS2XGBoostPredictor.pkl')
    if not os.path.exists(path):
        ds2_xgb_predictor.train_model(path)
    
    ds2_xgb_prediction = ds2_xgb_predictor.predict(nearest_neighbor_row_ds2, path)
    evaluator.add_prediction(ds2_xgb_prediction, weight=0.3)

def calculate_risk(medical_data):
    with open(os.path.join('ml/includes', 'common_columns.json')) as f:
        common_columns = json.load(f)
    data_processor = DataInputer(common_columns)
    validated_data = data_processor.get_valid_input(medical_data)
    query_ds2, query_ds4 = data_processor.prepare_queries(validated_data)
    
    ds2(common_columns, query_ds2)
    
    ds4(common_columns, query_ds4)
    
    return evaluator