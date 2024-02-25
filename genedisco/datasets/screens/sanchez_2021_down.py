import os
import numpy as np
import pandas as pd
import slingpy as sp
from genedisco.datasets.features.hgnc_names import HGNCNames
from slingpy.data_access.data_sources.hdf5_tools import HDF5Tools
from slingpy.data_access.data_sources.hdf5_data_source import HDF5DataSource
from slingpy.data_access.data_sources.abstract_data_source import AbstractDataSource


class Sanchez2021Down(object):
    """
    Unpublished data from: Steinhart et al. 2024
    """
    @staticmethod
    def load_data(save_directory) -> AbstractDataSource:
        screen_name = 'sanchez_2021_down'
        h5_file = os.path.join(save_directory, f"sanchez_2021_down.h5")
        if not os.path.exists(h5_file):
            df = pd.read_csv(f'/dfs/user/yhr/AI_RA/research_assistant/datasets/ground_truth_Sanchez21_down.csv')
            df = df.rename(columns={'0':'Gene_name', '1':'Score'})

            df = df.set_index('Gene_name')
	    
            gene_names = df.index.values.tolist()
            name_converter = HGNCNames(save_directory)
            gene_names = name_converter.update_outdated_gene_names(gene_names)
            df.index = gene_names

            # Merge duplicate indices by averaging
            df = df.groupby(df.index).mean()
            gene_names, data = df.index.values.tolist(), df[['Score']].values.astype(np.float32)


            HDF5Tools.save_h5_file(h5_file,
                                     data,
                                    f"sanchez_2021_down.h5",
                                    column_names=["Score"],
                                    row_names=gene_names)
        data_source = HDF5DataSource(h5_file, duplicate_merge_strategy=sp.MeanMergeStrategy())
        return data_source
