import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.exceptions import CustomException
import src.logger as logger
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    def get_data_transformer_object(self):
        try:
            logger.logging.info("Data Transformation initiated")
            numerical_columns = ['reading_score', 'writing_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            num_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )
            logger.logging.info("Numerical and categorical pipeline completed")
            preprocessor=ColumnTransformer(
                [
                    ('num_pipelines',num_pipeline,numerical_columns),
                    ('cat_pipelines',cat_pipeline,categorical_columns)
                ]
            )
            return preprocessor
            
        except:
            logger.logging.info("Exception occurred in data transformation")
            raise CustomException(sys.exc_info())
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)  
            logger.logging.info("Read train and test data completed")
            logger.logging.info("Obtaining preprocessor object")
            preprocessing_obj=self.get_data_transformer_object()
            target_column_name='math_score'
            numerical_columns = ['reading_score', 'writing_score']
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            train_arr=np.c_[preprocessing_obj.fit_transform(input_feature_train_df),np.array(target_feature_train_df)]
            test_arr=np.c_[preprocessing_obj.transform(input_feature_test_df),np.array(target_feature_test_df)]

            logger.logging.info("Saved preprocessing object")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            logger.logging.info("Exception occurred in data transformation")
            raise CustomException(e, sys.exc_info())