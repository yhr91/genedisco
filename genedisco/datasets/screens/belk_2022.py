"""
Copyright 2021 Patrick Schwab, Arash Mehrjou, GlaxoSmithKline plc; Andrew Jesson, University of Oxford; Ashkan Soleymani, MIT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import numpy as np
import pandas as pd
import slingpy as sp
from genedisco.datasets.features.hgnc_names import HGNCNames
from slingpy.data_access.data_sources.hdf5_tools import HDF5Tools
from slingpy.data_access.data_sources.hdf5_data_source import HDF5DataSource
from slingpy.data_access.data_sources.abstract_data_source import AbstractDataSource


class Belk2022(object):
    """
    """
    @staticmethod
    def load_data(save_directory) -> AbstractDataSource:
        screen_name = 'belk_2022'
        h5_file = os.path.join(save_directory, f"belk_2022.h5")
        if not os.path.exists(h5_file):
            df = pd.read_csv(f'/dfs/user/yhr/AI_RA/research_assistant/datasets/ground_truth_Belk22.csv')
            df = df.set_index('Gene')

            gene_names = df.index.values.tolist()
            name_converter = HGNCNames(save_directory)
            gene_names = name_converter.update_outdated_gene_names(gene_names)
            df.index = gene_names

            # Merge duplicate indices by averaging
            df = df.groupby(df.index).mean()
            gene_names, data = df.index.values.tolist(), df[['Score']].values.astype(np.float32)


            HDF5Tools.save_h5_file(h5_file,
                                     data,
                                    f"belk_2022.h5",
                                    column_names=["Score"],
                                    row_names=gene_names)
        data_source = HDF5DataSource(h5_file, duplicate_merge_strategy=sp.MeanMergeStrategy())
        return data_source
