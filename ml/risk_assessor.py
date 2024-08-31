import time
import pandas as pd

from ml.data_inputer import DataInputer

from ml.ds2.ds2_preprocessor import DS2PreProcessor
from ml.ds4.ds4_pre_processor import DS4PreProcessor

from ml.ds2.ds2_xgboost_predictor import DS2XGBoostPredictor
from ml.ds2.ds2_svm_predictor import DS2SVMPredictor
from ml.ds2.ds2_extra_tree_predictor import DS2ExtraTreePredictor
from ml.ds2.ds2_decision_tree_predictor import DS2DecisionTreePredictor

from ml.ds4.ds4_nn_predictor import DS4NNPredictor
from ml.ds4.ds4_naive_bayes_predictor import DS4NaiveBayesPredictor
from ml.ds4.ds4_linear_svm_predictor import DS4LinearSVMPredictor
from ml.ds4.ds4_xgboost_predictor import DS4XGBoostPredictor

from ml.knn_data_processor import KNNDataProcessor
from ml.prediction_evaluator import PredictionEvaluator
from ml.predictor import Predictor

from ml.s3_file_manager import file_manager

class RiskAssessor:
    def __init__(self, data_inputer: DataInputer, common_columns):
        self.__data_inputer = data_inputer
        self.__common_columns = common_columns
        
        df2 = file_manager.fetch_csv('dataset2.csv')
        self.__ds2_preprocessor = DS2PreProcessor(df2)
        
        df4 = file_manager.fetch_csv('dataset4.csv')
        self.__ds4_preprocessor = DS4PreProcessor(df4)
        
    def calculate_risk(self, query=None, ds2_doctor_vote=1, ds4_doctor_vote=1):
        evaluator = PredictionEvaluator(
            ds2={ "doctor_votes": ds2_doctor_vote, "num_rows": self.__ds2_preprocessor.number_of_rows() },
            ds4={ "doctor_votes": ds4_doctor_vote, "num_rows": self.__ds4_preprocessor.number_of_rows() }
        )
        query_ds2, query_ds4 = self.__data_inputer.prepare_queries(query)
        self.__ds2(evaluator, query_ds2)
        self.__ds4(evaluator, query_ds4)
        return evaluator.evaluate_risk_assessment()

    def __ds2(self, evaluator: PredictionEvaluator, query_ds2):
        start_time = time.time()

        print(f"knn_data_processor_ds2")
        knn_data_processor_ds2 = KNNDataProcessor(self.__common_columns, self.__ds2_preprocessor.get_preprocessed_data, "ds2", query_ds2)
        nearest_neighbor_row_ds2 = knn_data_processor_ds2.find_nearest_neighbor()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.2f} seconds")

        predictors = [
            DS2XGBoostPredictor(self.__ds2_preprocessor, 'DS2XGBoostPredictor.pkl'),
            DS2SVMPredictor(self.__ds2_preprocessor, 'DS2SVMPredictor.pkl'),
            DS2ExtraTreePredictor(self.__ds2_preprocessor, 'DS2ExtraTreePredictor.keras'),
            DS2DecisionTreePredictor(self.__ds2_preprocessor, 'DS2DecisionTreePredictor.pkl')
        ]
        for predictor in predictors:
            self.__run_predictor('VITAL_STATUS', "ds2", nearest_neighbor_row_ds2, predictor, evaluator)

    def __ds4(self, evaluator: PredictionEvaluator, query_ds4):
        start_time = time.time()
        print(f"knn_data_processor_ds4")
        knn_data_processor_ds4 = KNNDataProcessor(self.__common_columns, self.__ds4_preprocessor.get_preprocessed_data, "ds4", query_ds4)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.2f} seconds")

        start_time = time.time()
        print(f"find_nearest_neighbor")
        nearest_neighbor_row_ds4 = knn_data_processor_ds4.find_nearest_neighbor()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.2f} seconds")

        predictors = [
            DS4NNPredictor(self.__ds4_preprocessor, 'DS4NNPredictor.keras'),
            DS4NaiveBayesPredictor(self.__ds4_preprocessor, 'DS4NaiveBayesPredictor.pkl'),
            DS4LinearSVMPredictor(self.__ds4_preprocessor, 'DS4LinearSVMPredictor.pkl'),
            DS4XGBoostPredictor(self.__ds4_preprocessor, 'DS4XGBoostPredictor.pkl')
        ]
        for predictor in predictors:
            self.__run_predictor('hospital_death', "ds4", nearest_neighbor_row_ds4, predictor, evaluator)
    
    def __run_predictor(self, target_column: str, ds_name: str, nearest_neighbor_row: pd.Series, predictor: Predictor, evaluator: PredictionEvaluator):
        start_time = time.time()

        print(f"Predicting {target_column} using {predictor.__class__.__name__} on {ds_name}")
        predictor.train_model()
        prediction = predictor.predict(nearest_neighbor_row)
        evaluation = predictor.evaluate_model()
        evaluator.add_prediction(prediction, evaluation, ds_name)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.2f} seconds")
