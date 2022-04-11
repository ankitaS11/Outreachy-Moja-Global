import os

import geopandas as gpd
import matplotlib.pyplot as plt


class Dataset:
    """
    Sample Dataset class which will load + process the dataset.
    
    Note that the process_dataset method is virtual, and needs to be implemented by child classes.
    """
    def __init__(self, path):
        self.path = path
        self.df = None

    def load_dataset(self):
        """
        Returns and saves the dataset after loading into a dataframe.
        
        Will raise an AssertionError if the path (passed during initialization) doesn't exist anymore.
        """
        # First ensure that the path exists!
        path = self.path
        assert os.path.exists(path), f"The given path: {path} does not exist."
        
        # Load the dataset into a GeoDataFrame
        self.df = gpd.read_file(path)
        
        print("Dataset loaded successfully with number of rows: ", len(self.df))
        return self.df

    def _get_index(self, ind):
        return self.df.iloc[ind]

    def __getitem__(self, index):
        assert self.df is not None, "Dataset has not been loaded yet. Please do obj.load_dataset()"
        return self._get_index(index)
    
    def process_dataset(self, *args, **kwargs):
        # virtual method, implement in the child class
        # df_base is common for all, as we will have to clip the dataframe always! (only for this EDA)
        raise NotImplementedError("This class needs to be implemented by the child class.")
    
    def plot(self, *args, **kwargs):
        # virtual method, implement in the child class
        raise NotImplementedError("This class needs to be implemented by the child class.")


class SoilClass(Dataset):
    def process_dataset(self, *args, **kwargs):
        df_base = kwargs.get("df_reference", None)
        if df_base is None:
            raise ValueError("Expected a df_reference= kwarg, but got none")
        output_df = self.df.clip(df_base)
        self.df = output_df
        return output_df
    
    def plot(self, show=True, save_output=True, *args, **kwargs):
        df_ref = kwargs.get("df_reference", None)
        if df_ref is None:
            raise ValueError("Expected a df_reference= kwarg, but got none")
        fig, ax = plt.subplots(1, 1, figsize=(20, 10));
        df_ref.plot(ax=ax, color='none')
        ax.set_title("Tropical Dry Forest (RED) in INDIA")
        self.df.plot(ax=ax, color='red')
        if show:
            plt.axis('off')
            plt.show()
        if save_output:
            plt.savefig('soil_cover.png')
            print("File saved to soil_cover.png.")

class EcologicalClass(Dataset):
    def process_dataset(self, *args, **kwargs):
        df_base = kwargs.get("df_reference", None)
        if df_base is None:
            raise ValueError("Expected a df_reference= kwarg, but got none")
        output_df = self.df.clip(df_base)
        self.df = output_df
        return output_df

    def plot(self, show=True, save_output=True, *args, **kwargs):
        df_ref = kwargs.get("df_reference", None)
        if df_ref is None:
            raise ValueError("Expected a df_reference= kwarg, but got none")
        fig, ax = plt.subplots(1, 1, figsize=(20, 10));
        df_ref.plot(ax=ax, color='none', legend=True)
        ax.set_title("Ecological Zones in Tropical Dry Forest portions in India")
        self.df.plot(ax=ax, column='gez_name', legend=True)
        if show:
            plt.axis('off')
            plt.show()
        if save_output:
            plt.savefig('ecological_zone.png')
            print("File saved to ecological_zone.png.")

class ClimateClass(Dataset):
    def process_dataset(self, *args, **kwargs):
        df_base = kwargs.get("df_reference", None)
        if df_base is None:
            raise ValueError("Expected a df_reference= kwarg, but got none")

        class_names_dict = {
            11: 'Tropical rainforest climate', 12: 'Tropical monsoon climate',
            10: 'Cool Temperature Moist', 0: 'Oceans', 1: 'Warm Temperature Moist',
            9: 'Tropical Montane'
        }

        # Map class names (encoded in numbers) to strings (meaningful)
        self.df.CLASS_NAME = self.df.CLASS_NAME.map(class_names_dict).fillna(self.df.CLASS_NAME)
        
        # Clip the dataframe to get our relevant dataset
        output_df = self.df.clip(df_base)
        self.df = output_df
        return output_df
    
    def plot(self, show=True, save_output=True, *args, **kwargs):
        df_ref = kwargs.get("df_reference", None)
        if df_ref is None:
            raise ValueError("Expected a df_reference= kwarg, but got none")
        fig, ax = plt.subplots(1, 1, figsize=(20, 10));
        df_ref.plot(ax=ax, color='none', legend=True)
        ax.set_title("Climate Zones in Tropical Dry Forest portions in India")
        self.df.plot(ax=ax, column='CLASS_NAME', cmap="PRGn", legend=True)
        if show:
            plt.axis('off')
            plt.show()
        if save_output:
            plt.savefig('climate.png')
            print("File saved to climate.png.")