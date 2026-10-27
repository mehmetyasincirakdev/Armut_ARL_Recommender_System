import unittest

import pandas as pd

from armut_recommender import prepare_data, recommend_for_user


class RecommendationTests(unittest.TestCase):
    def setUp(self):
        rows = []
        baskets = [
            (10, "2024-01", (1, 2)),
            (10, "2024-02", (1, 2)),
            (20, "2024-01", (1, 3)),
            (30, "2024-01", (1, 3)),
        ]
        for user_id, month, services in baskets:
            for service_id in services:
                rows.append(
                    {
                        "UserId": user_id,
                        "ServiceId": service_id,
                        "CategoryId": 1,
                        "CreateDate": f"{month}-15",
                    }
                )
        self.data = prepare_data(pd.DataFrame(rows))

    def test_recommends_items_from_rules_for_latest_basket(self):
        recommendations = recommend_for_user(
            self.data,
            "10",
            min_support=0.25,
            min_confidence=0.5,
        )

        self.assertIn("3_1", recommendations["service"].tolist())
        self.assertNotIn("1_1", recommendations["service"].tolist())
        self.assertNotIn("2_1", recommendations["service"].tolist())

    def test_unknown_user_has_no_recommendations(self):
        recommendations = recommend_for_user(self.data, "unknown")

        self.assertTrue(recommendations.empty)

    def test_rejects_invalid_support(self):
        with self.assertRaisesRegex(ValueError, "min_support"):
            recommend_for_user(self.data, "10", min_support=0)


if __name__ == "__main__":
    unittest.main()
