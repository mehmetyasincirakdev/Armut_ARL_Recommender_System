import unittest

import pandas as pd

from armut_recommender import build_basket_matrix, prepare_data


class PrepareDataTests(unittest.TestCase):
    def test_builds_service_and_monthly_basket_identifiers(self):
        raw_data = pd.DataFrame(
            [
                {
                    "UserId": 10,
                    "ServiceId": 20,
                    "CategoryId": 3,
                    "CreateDate": "2024-01-15",
                }
            ]
        )

        prepared = prepare_data(raw_data)

        self.assertEqual(prepared.loc[0, "Service"], "20_3")
        self.assertEqual(prepared.loc[0, "YearMonth"], "2024-01")
        self.assertEqual(prepared.loc[0, "BasketID"], "10_2024-01")

    def test_rejects_missing_required_columns(self):
        with self.assertRaisesRegex(ValueError, "missing required columns"):
            prepare_data(pd.DataFrame({"UserId": [10]}))

    def test_rejects_rows_with_invalid_required_values(self):
        raw_data = pd.DataFrame(
            [
                {
                    "UserId": 10,
                    "ServiceId": 20,
                    "CategoryId": 3,
                    "CreateDate": "not-a-date",
                }
            ]
        )

        with self.assertRaisesRegex(ValueError, "invalid CreateDate"):
            prepare_data(raw_data)

    def test_basket_matrix_contains_boolean_service_presence(self):
        prepared = prepare_data(
            pd.DataFrame(
                [
                    {
                        "UserId": 10,
                        "ServiceId": 20,
                        "CategoryId": 3,
                        "CreateDate": "2024-01-15",
                    },
                    {
                        "UserId": 10,
                        "ServiceId": 20,
                        "CategoryId": 3,
                        "CreateDate": "2024-01-20",
                    },
                ]
            )
        )

        baskets = build_basket_matrix(prepared)

        self.assertEqual(baskets.shape, (1, 1))
        self.assertTrue(bool(baskets.loc["10_2024-01", "20_3"]))


if __name__ == "__main__":
    unittest.main()
