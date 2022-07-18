import pandas as pd

class ColumnProfiling:
    """
    Input : Pandas DataFrame
    Output : Nested dictionnary with descriptives for each feature containing :
                - Count and Percentage of Missing Values
                - Data type
                - General Descriptives Mean, Median etc.
                - Proportion of Duplicates
                - etc.
    """ 
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.state = {}
        
    def create_dictionnary(self):
        for column in self.df :
            self.state[column] = {}
        return self.state, self.df

    def has_nan(self):
        self.state, self.df = self.create_dictionnary()
        for key in self.state.keys():
            self.state[key]['hasnans'] = self.df[key].hasnans
            if self.df[key].empty:
                self.state[key]["hasnans"] = 'empty'

        return self.state, self.df
    
    def get_missing_values(self):
        # Has an issue
        self.state, self.df = self.has_nan()
        total_ = self.df.shape[0]
        for key in self.state.keys():
            mv_ = self.df[key].isna().sum()
            self.state[key]['missing_value_count'] = mv_
            self.state[key]['missing_value_pct'] = mv_/total_
        return self.state, self.df
    
    def get_cardinality(self):
        # Add data format
        # Format dtypes : O = String etc.
        self.state, self.df = self.get_missing_values()
        for key in self.state.keys():
            self.state[key]['cardinality'] = self.df[key].nunique() / self.df.shape[0]
        return self.state, self.df
    
    def get_majority_class(self):
        self.state, self.df = self.get_cardinality()
        for key in self.state.keys():
                self.df[key] = self.df[key].fillna('Missing')
                sub = self.df[key].value_counts()/self.df.shape[0]
                tiles = {}
                for i in range(len(sub)):
                    if sub[i] > 0.03:
                        tiles[sub.index[i]] = sub[i]
                    else :
                        break
                self.state[key]['majority_class'] = tiles
        return self.state, self.df

    
    def get_data_type(self):
        # Add data format
        # Format dtypes : O = String etc.
        self.state, self.df = self.get_majority_class()
        for key in self.state.keys():
            self.state[key]['dtype'] = str(self.df[key].convert_dtypes().dtype)
        return self.state, self.df
    
    def get_descriptives(self):
        self.state, self.df = self.get_data_type()
        for key in self.state.keys():
            if 'float' in self.state[key]['dtype'].lower() or 'int' in self.state[key]['dtype'].lower()  : 
                self.state[key]['descriptives'] = {'mean' : self.df[key].mean(),
                                                   'std' : self.df[key].std(),
                                                   'min' : self.df[key].min(),
                                                   'max' : self.df[key].max()
                                                    # add median and quartiles 
                                                    }
        return self.state, self.df
        
    def get_duplicates(self):
        pass
    
    def get_list_of_common_duplicates(self):
        pass
    
    def get_strongly_correlated_variables(self):
        pass
    
    def get_highly_correlating_features(self):
        pass
    
    def get_memory_usage(self):
        pass
    
class DatasetProfiling:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.state = {}

if __name__ == "__main__":
    df = pd.read_csv("https://data.cityofchicago.org/api/views/xzkq-xp2w/rows.csv?accessType=DOWNLOAD")
    pro = ColumnProfiling(df)
    state_, df_ = pro.get_data_type()
    print(state_)