from typing import List, Tuple, Dict
import numpy as np
from numpy.lib import recfunctions as rfn
import pandas as pd
from frds.data import Dataset
from frds.measures import CorporateFinanceMeasure
from frds.data.utils import filter_funda


NAME = "FirmSize"
DATASETS_REQUIRED: List[Dataset] = [
    Dataset(
        source="wrds",
        library="comp",
        table="funda",
        vars=[
            "datadate",
            "gvkey",
            "at",
            "indfmt",
            "datafmt",
            "popsrc",
            "consol",
        ],
        date_vars=["datadate"],
    )
]
VARIABLE_LABELS = {NAME: "Natural logarithm of total assets"}


class FirmSize(CorporateFinanceMeasure):
    """Firm size: the natural logarithm of total assets"""

    url_docs = "https://frds.io/measures/firm_size/"

    def __init__(self):
        super().__init__("Firm Size", DATASETS_REQUIRED)

    def estimate(self, nparrays: List[np.recarray]):
        nparray = filter_funda(nparrays[0])
        size = np.log(nparray.at, where=(nparray.at > 0))
        size[np.isnan(nparray.at)] = np.nan
        nparray = rfn.rec_append_fields(nparray, NAME, size)
        # keep only useful columns
        cols = set(rfn.get_names_flat(nparray.dtype))
        nparray.sort(order=(keys := ["gvkey", "datadate"]))
        exclude_cols = cols - set([*keys, "at", NAME])
        return (
            pd.DataFrame.from_records(nparray, exclude=exclude_cols),
            VARIABLE_LABELS,
        )
