#!/usr/bin/env python3
"""Arxiv data set."""

from dataclasses import dataclass
from logging import debug
from pathlib import Path
from typing import Any

import pandas as pd

from arxiv_categories import ArxivCategory


class DataSet:
    """This class represents the "Nature Data Set"."""

    @dataclass
    class Parameters:
        """Represent the necessary properties to load a dataset."""

        date_interval: tuple[pd.Timestamp, pd.Timestamp]
        categories: list[ArxivCategory]
        max_num_of_authors: int

    def __init__(self, data_set_properties: Parameters) -> None:
        """Create data set without loading data."""
        self._data_set_properties = data_set_properties
        self._documents: pd.DataFrame = pd.DataFrame()

    def info(self) -> dict[str, Any]:
        """Return a dict representation based on the network properties."""
        if ArxivCategory.ALL in self._data_set_properties.categories:
            categories = 'Not filtered'
        else:
            categories = [category.name for category in self._data_set_properties.categories]

        result: dict[str, Any] = {
            'categories': categories,
            'num_of_documents': len(self.documents),
        }
        return result

    def load_data(self, data_file_name: Path) -> None:
        """Load data from the disk for further processing."""
        # the dataset contains integers as node ids
        debug(f'Loading data file {str(data_file_name)}...')
        documents = pd.read_csv(
            data_file_name,
            index_col=0,
            parse_dates=['publish_time'],
            low_memory=False
        )
        debug('Loading data file done')
        documents['authors'] = documents['authors'].apply(eval).apply(set).apply(list)

        self._documents = documents

    def get_data(self, dataset_properties: Parameters) -> None:
        """Filter the data set by date."""
        documents = self._documents

        # filtering
        documents = documents[
            documents['authors'].map(len) <= dataset_properties.max_num_of_authors
        ]

        if ArxivCategory.ALL not in dataset_properties.categories:
            documents = documents[
                documents['category'].isin([
                    category.value for category in self._data_set_properties.categories
                ])
            ]

        return documents[
            (documents['publish_time'] >= dataset_properties.date_interval[0]) &
            (documents['publish_time'] < dataset_properties.date_interval[1])
        ]
