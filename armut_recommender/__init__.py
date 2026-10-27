"""Armut association-rule recommendation package."""

from armut_recommender.baskets import build_basket_matrix
from armut_recommender.data import DEFAULT_DATASET_PATH, load_data, prepare_data
from armut_recommender.recommendations import recommend_for_user

__all__ = [
    "DEFAULT_DATASET_PATH",
    "build_basket_matrix",
    "load_data",
    "prepare_data",
    "recommend_for_user",
]
