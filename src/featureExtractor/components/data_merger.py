import pandas as pd 


class DataMerger:
    def __init__(self,prev_df,new_df):
        self.prev_df = prev_df
        self.new_df = new_df
        self.data = None

    def merge(self):
        self.data = self.prev_df.join(self.new_df,on='image_link')
        return self.data

    