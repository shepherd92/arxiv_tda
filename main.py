#!/usr/bin/env python3
"""This module is responsible for building a simplicial complex from a dataset."""

from datetime import datetime, UTC
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from arxiv_categories import ArxivCategory
from data_set import DataSet
from simplicial_complex import SimplicialComplex


MAX_SIMPLEX_DIMENSION = 2  # maximum dimension of the simplices to be created; beware of combinatorial explosion
DATA_SET_PARAMETERS = DataSet.Parameters(
    date_interval=(pd.Timestamp('1900-01-01', tz='UTC'), pd.Timestamp('2025-01-01', tz='UTC')),  # filter for other dates
    categories=[ArxivCategory.ALL],  # filter for other categories, look at arxiv_categories.py
    max_num_of_authors=10,  # do not include documents with more than 10 authors; beware of combinatorial explosion
)


def main(data_set_parameters: DataSet.Parameters) -> None:
    """Run program - main function."""
    
    # create the output directory
    now = datetime.now(UTC).strftime('%Y%m%d_%H%M%S')
    output_dir = Path('output') / now
    output_dir.mkdir(parents=True, exist_ok=True)

    # load the data set
    data_set = DataSet(data_set_parameters)
    data_set.load_data(Path('data/documents.csv'))

    intervals = generate_intervals(
        start=pd.Timestamp('2008-01-01', tz='UTC'),
        end=data_set_parameters.date_interval[1],
        window=pd.Timedelta(days=365),
        stride=pd.Timedelta(days=30))  # generate intervals of one year
    
    for interval in intervals:
        dataset_properties = DataSet.Parameters(
            date_interval=interval,
            categories=[ArxivCategory.ALL],
            max_num_of_authors=10
        )
        current_data = data_set.get_data(dataset_properties)
        print(f'\rProcessing interval: {interval[0].year}_{interval[0].month}_{interval[0].day} - {interval[1].year}_{interval[1].month}_{interval[1].day}', end='')
        if current_data.empty:
            continue

        simplicial_complex = SimplicialComplex(MAX_SIMPLEX_DIMENSION)
        simplicial_complex.build(current_data)
        simplicial_complex.compute_persistence()
        persistence_diagram : plt.Figure = simplicial_complex.create_persistence_diagram(x_min=0., y_min=0., x_max=50., y_max=50.)

        persistence_diagram.savefig(output_dir / f'persistence_diagram_{interval[0].year}_{interval[0].month}_{interval[0].day}.png')

    # analyze the simplicial complex
    betti_numbers: list[int] = simplicial_complex.betti_numbers()

    print('Done.')


def generate_intervals(
        start: pd.Timestamp,
        end: pd.Timestamp,
        window: pd.Timedelta,
        stride: pd.Timedelta
    ) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Generate intervals for the given start and end timestamps with the specified step."""
    intervals = [(current_start, current_start + window) for current_start in pd.date_range(start, end, freq=stride)]
    return intervals


if __name__ == '__main__':
    main(DATA_SET_PARAMETERS)
