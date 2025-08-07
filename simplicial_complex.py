#!/usr/bin/env python3
"""Simplicial complex"""

from collections import defaultdict
from itertools import combinations

import pandas as pd
from gudhi import plot_persistence_diagram
from gudhi.simplex_tree import SimplexTree
from matplotlib import pyplot as plt
from tqdm import tqdm


class SimplicialComplex:
    """This class represents a simplicial complex."""

    def __init__(self, max_dimension: int) -> None:
        assert type(max_dimension) == int, \
            f'MAX_SIMPLEX_DIMENSION must be an integer, but it is {type(max_dimension)}'
        assert max_dimension >= 0, \
            f'MAX_SIMPLEX_DIMENSION must be non-negative, but it is {max_dimension}'
        self.max_dimension = max_dimension
        self.simplex_tree = SimplexTree()
    
    def build(self, documents: pd.DataFrame) -> None:
        face_counts = defaultdict(int)
        for simplex in tqdm(documents['authors'], desc='Processing authors ', delay=1):
        # for simplex in [[1, 20, 3], [1, 20]]:
            num_of_authors_in_simplex = len(simplex)
            for face_dimension in range(0, num_of_authors_in_simplex):  # All non-empty subsets
                for face in combinations(simplex, min(face_dimension + 1, self.max_dimension + 1)):
                    face_counts[tuple(sorted(face))] += 1

        self.simplex_tree.set_dimension(self.max_dimension)
        for face, count in tqdm(face_counts.items(), desc='Inserting simplices', delay=1):
            self.simplex_tree.insert(face, filtration=50 - count)

        self.simplex_tree.make_filtration_non_decreasing()

    def create_persistence_diagram(self, x_min=None, x_max=None, y_min=None, y_max=None) -> plt.Figure:
        figure, axes = plt.subplots()

        # Separate finite and infinite points
        finite_pts = [pt for pt in self._persistence if pt[1][1] != float('inf')]
        inf_pts = [pt for pt in self._persistence if pt[1][1] == float('inf')]

        # Plot finite points by dimension
        for dim in set(d for d, _ in finite_pts):
            xs = [b for d, (b, dth) in finite_pts if d == dim]
            ys = [dth for d, (b, dth) in finite_pts if d == dim]
            axes.scatter(xs, ys, label=f"H{dim}")

        # Compute data range
        all_births = [b for _, (b, _) in self._persistence if b != float('inf')]
        all_deaths = [d for _, (_, d) in finite_pts]
        data_min = min(all_births + all_deaths) if all_births + all_deaths else 0.0
        data_max = max(all_births + all_deaths) if all_births + all_deaths else 1.0

        # Use manual limits if provided
        x_min = x_min if x_min is not None else data_min
        x_max = x_max if x_max is not None else data_max
        y_min = y_min if y_min is not None else data_min
        y_max = y_max if y_max is not None else data_max

        # Make square: expand smaller range
        total_min = min(x_min, y_min)
        total_max = max(x_max, y_max)
        x_min = y_min = total_min
        x_max = y_max = total_max

        # Plot infinite death points as upward triangles, but skip label
        if inf_pts:
            inf_y = y_max + 0.1  # plot slightly above visible range
            for dim in set(d for d, _ in inf_pts):
                xs = [b for d, (b, _) in inf_pts if d == dim]
                ys = [inf_y for _ in xs]
                axes.scatter(xs, ys, marker='^')  # no label

        # Plot diagonal
        axes.plot([total_min, total_max], [total_min, total_max], "k--", alpha=0.5)

        # Set plot properties
        axes.set_xlim(x_min, x_max)
        axes.set_ylim(y_min, y_max + 0.2)  # room for ∞ markers
        axes.set_title("Persistence diagram")
        axes.set_xlabel("Birth")
        axes.set_ylabel("Death")
        axes.set_aspect('equal', adjustable='box')
        axes.legend()

        return figure

    def compute_persistence(self) -> None:
        """Compute the persistence of the simplicial complex."""
        self.simplex_tree.compute_persistence(persistence_dim_max=True)

    def betti_numbers(self) -> list[int]:
        """Return the Betti numbers of the simplicial complex."""
        return self.simplex_tree.betti_numbers()

    def print_info(self) -> None:
        """Print information about the simplicial complex."""
        print('Simplicial complex info:')
        print(f'  Number of vertices: {self.simplex_tree.num_vertices()}')
        print(f'  Number of simplices: {self.simplex_tree.num_simplices()}')

    @property
    def _persistence(self) -> list[tuple[int, tuple[int, int]]]:
        """Compute the persistence of the simplicial complex."""
        return self.simplex_tree.persistence()
