from attritionRate.utils import load_object 
import pandas as pd
import os

class AttritionRateData:
    def __init__(self,
                table_id: int,
                name: object,
                phone_number: int,
                location: object,
                emp_group: object,
                function: object,
                gender: object,
                tenure: float,
                tenure_grp: object,
                experience_yymm: float,
                marital_status: object,
                age_in_yy: float,
                hiring_source: object,
                promoted_non_promoted: object,
                job_role_match: object,
                stay_left: object = None,
                 ):
        self.table_id = table_id
        self.name = name
        self.phone_number = phone_number
        self.location = location
        self.emp_group = emp_group
        self.function = function
        self.gender = gender
        self.tenure = tenure
        self.tenure_grp = tenure_grp
        self.experience_yymm = experience_yymm
        self.marital_status = marital_status
        self.age_in_yy = age_in_yy
        self.hiring_source = hiring_source
        self.promoted_non_promoted = promoted_non_promoted
        self.job_role_match = job_role_match
        self.stay_left = stay_left
        
    def get_inputuser_dataframe(self):
        user_data = self.get_inputuser_dataframe_as_dict()
        return pd.DataFrame(user_data)
    
    def get_inputuser_dataframe_as_dict(self):
        input_userdata = {
            "table_id" : [self.table_id],
            "name" : [self.name] ,
            "phone_number" : [self.phone_number],
            "location" : [self.location],
            "emp_group" : [self.emp_group],
            "function" : [self.function],
            "gender" : [self.gender],
            "tenure" : [self.tenure],
            "tenure_grp" : [self.tenure_grp],
            "experience_yymm" : [self.experience_yymm],
            "marital_status" : [self.marital_status],
            "age_in_yy" : [self.age_in_yy],
            "hiring_source" : [self.hiring_source],
            "promoted_non_promoted" : [self.promoted_non_promoted],
            "job_role_match" : [self.job_role_match],
            }
        return input_userdata
        
        
class AttritionRateEstimator:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        
    def get_latest_model_path(self):
        folder_name = list(map(int, os.listdir(self.model_dir)))
        latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
        file_name = os.listdir(latest_model_dir)[0]
        latest_model_path = os.path.join(latest_model_dir, file_name)
        return latest_model_path
    
    def predict(self, X):
        model_path = self.get_latest_model_path()
        model = load_object(model_path)
        stay_left = model.predict(X)
        return stay_left
        
        
        