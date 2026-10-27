"""Command-line interface for service recommendations."""

import argparse
from pathlib import Path

from armut_recommender.data import DEFAULT_DATASET_PATH, load_data
from armut_recommender.recommendations import recommend_for_user


def _probability(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("value must be a number between 0 and 1") from error
    if not 0 <= parsed <= 1:
        raise argparse.ArgumentTypeError("value must be between 0 and 1")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser used by the command-line entry points."""
    parser = argparse.ArgumentParser(
        description="Recommend services from association rules and a user's latest basket."
    )
    parser.add_argument("--user-id", required=True, help="User ID to generate recommendations for.")
    parser.add_argument(
        "--data-path",
        type=Path,
        default=DEFAULT_DATASET_PATH,
        help="Path to a local CSV dataset (default: Datasets/armut_data.csv).",
    )
    parser.add_argument(
        "--min-support",
        type=_probability,
        default=0.01,
        help="Minimum itemset support between 0 and 1 (default: 0.01).",
    )
    parser.add_argument(
        "--min-confidence",
        type=_probability,
        default=0.1,
        help="Minimum rule confidence between 0 and 1 (default: 0.1).",
    )
    parser.add_argument("--top-n", type=int, default=5, help="Maximum number of results.")
    return parser


def main(argv: list[str] | None = None) -> None:
    """Parse command-line arguments and print service recommendations."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.min_support == 0:
        parser.error("--min-support must be greater than 0")
    if args.top_n < 1:
        parser.error("--top-n must be at least 1")

    data = load_data(args.data_path)
    recommendations = recommend_for_user(
        data,
        args.user_id,
        min_support=args.min_support,
        min_confidence=args.min_confidence,
        top_n=args.top_n,
    )
    if recommendations.empty:
        print(f"No recommendations found for user {args.user_id}.")
        return

    print(recommendations.to_string(index=False))
