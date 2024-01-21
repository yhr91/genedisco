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
    Data from: CRISPR activation and interference screens in primary human T cells decode cytokine
    regulation. bioRxiv 2021
    https://www.biorxiv.org/content/10.1101/2021.05.11.443701v1
    GEOS URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174292

    Commands:
    mageck test -k GSE174255_reads_A.txt -t 32_DolcettoSetA_Donor1_IL2_high -c 31_DolcettoSetA_Donor1_IL2_low -n schmidt_il2_d1
    mageck test -k GSE174255_reads_A.txt -t 44_DolcettoSetA_Donor2_IL2_high -c 43_DolcettoSetA_Donor2_IL2_low -n schmidt_il2_d2

    LICENSE: https://www.ncbi.nlm.nih.gov/geo/info/disclaimer.html
    """
    @staticmethod
    def load_data(save_directory) -> AbstractDataSource:
        h5_file = os.path.join(save_directory, "belk_2022.h5")
        data_source = HDF5DataSource(h5_file, duplicate_merge_strategy=sp.MeanMergeStrategy())
        return data_source
