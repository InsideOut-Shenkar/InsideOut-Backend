import os
import joblib

from sklearn.svm import SVC 

from ml.predictor import Predictor
from ml.s3_file_manager import file_manager

class DS4SVMPredictor(Predictor):
    def __init__(self, preprocessor, path):
        super().__init__(preprocessor, path)

    def build_model(self, X_train, y_train):
        svm_model = SVC(probability=True)
        model = svm_model.fit(X_train, y_train)
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
