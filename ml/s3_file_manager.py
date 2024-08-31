import boto3
import joblib
import pandas as pd
import json
import os
from botocore.exceptions import NoCredentialsError
from tensorflow.keras.models import load_model as tensorflow_load_model

class S3FileManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(S3FileManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, buckets=None, aws_access_key_id=None, aws_secret_access_key=None):
        if not hasattr(self, 'initialized'):
            self.buckets = buckets
            self.local_files = {}
            self.initialized = True
            if aws_access_key_id and aws_secret_access_key:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key
                )
                self.__fetch_files()

    def set_s3_client(self, aws_access_key_id, aws_secret_access_key):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.__fetch_files()
    
    def __fetch_files(self):
        if self.buckets:
            local_dir = 'tmp'
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            for bucket, objects in self.buckets.items():
                for obj in objects:
                    local_path = os.path.join(local_dir, os.path.basename(obj))

                    try:
                        s3_obj = self.s3_client.head_object(Bucket=bucket, Key=obj)
                        s3_last_modified = s3_obj['LastModified']

                        if os.path.exists(local_path):
                            local_last_modified = os.path.getmtime(local_path)
                            if s3_last_modified.timestamp() > local_last_modified:
                                self.__download_file(bucket, obj, local_path)
                            else:
                                self.local_files[obj] = local_path
                        else:
                            self.__download_file(bucket, obj, local_path)

                    except NoCredentialsError:
                        print(f"Credentials not available for bucket {bucket}")

    def __download_file(self, bucket, obj, local_path):
        self.s3_client.download_file(bucket, obj, local_path)
        self.local_files[obj] = local_path

    def fetch_file(self, bucket, obj):
        local_path = os.path.join('tmp', os.path.basename(obj)) 
        self.s3_client.download_file(bucket, obj, local_path)
        self.local_files[obj] = local_path

    def get_file_path(self, obj):
        return self.local_files.get(obj)

    def fetch_json(self, obj):
        local_path = self.get_file_path(obj)
        with open(local_path, 'r') as f:
            return json.load(f)

    def fetch_csv(self, obj):
        local_path = self.get_file_path(obj)
        return pd.read_csv(local_path)

    def fetch_model(self, obj):
        local_path = self.get_file_path(obj)
        return joblib.load(local_path)
    
    def fetch_tensorflow_model(self, obj):
        local_path = self.get_file_path(obj)
        return tensorflow_load_model(local_path)
    
buckets = {
    'insideout-ml': [
        'DS2DecisionTreePredictor.pkl',
        'DS2ExtraTreePredictor.keras',
        'DS2SVMPredictor.pkl',
        'DS2XGBoostPredictor.pkl',
        'DS4NaiveBayesPredictor.pkl',
        'DS4NNPredictor.keras',
        'DS4LinearSVMPredictor.pkl',
        'DS4XGBoostPredictor.pkl'
    ],
    'insideout-files': [
        'common_columns.json',
        'dataset2.csv',
        'dataset4 dictionary.csv',
        'dataset4.csv'
    ]
}

file_manager = S3FileManager(
    buckets=buckets,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
