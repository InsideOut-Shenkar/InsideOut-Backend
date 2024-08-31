import os
import joblib

from sklearn.ensemble import ExtraTreesClassifier

from ml.predictor import Predictor
from ml.s3_file_manager import file_manager

class DS2ExtraTreePredictor(Predictor):
    def __init__(self, preprocessor, path):
        super().__init__(preprocessor, path)

    def build_model(self, X_train, y_train):
        extra_classifier =  ExtraTreesClassifier(n_estimators=100, random_state=42)
        model = extra_classifier.fit(X_train, y_train)
        return model

    def save_model(self, model_path):
        if model_path is None: return
        if '/' in model_path:
            os.makedirs(model_path[:model_path.rfind('/')], exist_ok=True)
        joblib.dump(self.model, model_path) 

    def load_model(self, model_path):
        if model_path is not None:
            return file_manager.fetch_model(model_path)
        return self.model
    
