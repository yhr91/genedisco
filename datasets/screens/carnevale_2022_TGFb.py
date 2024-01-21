import os
import numpy as np
import pandas as pd
import slingpy as sp
from genedisco.datasets.features.hgnc_names import HGNCNames
from slingpy.data_access.data_sources.hdf5_tools import HDF5Tools
from slingpy.data_access.data_sources.hdf5_data_source import HDF5DataSource
from slingpy.data_access.data_sources.abstract_data_source import AbstractDataSource


class Carnevale2022TGFb(object):
    """
    Data from: Carnevale et al. 2022
    """
    @staticmethod
    def load_data(save_directory) -> AbstractDataSource:
        screen_name = 'TGFb'
        h5_file = os.path.join(save_directory, "carnevale_2022_{}.h5".format(screen_name))
        if not os.path.exists(h5_file):
            df = pd.read_excel('/dfs/project/perturb-gnn/AI_RA/Carnevale22/41586_2022_5126_MOESM5_ESM.xlsx',
                           sheet_name=screen_name)
            df = df.set_index('id')

            df.index = df.index.astype('str')
            rows_to_drop = [v for v in df.index if 'CTRL' in v]
            rows_to_drop = [v for v in df.index if v[:4]=='2021']
            df = df.drop(rows_to_drop)

            gene_names = df.index.values.tolist()
            name_converter = HGNCNames(save_directory)
            gene_names = name_converter.update_outdated_gene_names(gene_names)
            df.index = gene_names

            # Merge duplicate indices by averaging
            df = df.groupby(df.index).mean()
            gene_names, data = df.index.values.tolist(), df[['pos|lfc']].values.astype(np.float32)


            HDF5Tools.save_h5_file(h5_file,
                                   data,
                                   "carnevale_2022_{}.h5".format(screen_name),
                                   column_names=["log-fold-change"],
                                   row_names=gene_names)
        data_source = HDF5DataSource(h5_file, duplicate_merge_strategy=sp.MeanMergeStrategy())
        return data_source
