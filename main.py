from featureExtractor.components.data_creation import DataCreation
from featureExtractor.components.data_merger import DataMerger
import pandas as pd

data_path = "D:\hackthons\ML-Challenge/artifacts\dataset/train.csv"
prev_df = pd.read_csv(data_path)

DataCreation = DataCreation(data_path)
DataCreation.load_data()
features , image_links =DataCreation.create_features()

dict = {"image_link":image_links , "features":features}

new_df = pd.DataFrame(dict)

data_merger = DataMerger(prev_df,new_df)
final_data = data_merger.merge()





