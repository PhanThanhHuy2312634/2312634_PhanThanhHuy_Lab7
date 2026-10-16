import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Basic order-total tests."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 2}), 100000)

    def test_calculate_total_for_multiple_items(self):
        self.assertEqual(
            self.app.calculate_order_total({"pho": 1, "bun": 1}),
            95000,
        )

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0.0)

    def test_calculate_total_ignores_unknown_items_and_negative_quantities(self):
        self.assertEqual(
            self.app.calculate_order_total({"unknown": 1, "pho": -1}),
            0.0,
        )


class TestMediumLevel(unittest.TestCase):
    """Promotion tests for online, offline, and operating-system cases."""

    def setUp(self):
        self.app = YummyApp(network_status="online", os_version=15)

    def test_apply_valid_promo_code_while_online(self):
        self.assertEqual(self.app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_apply_promo_code_while_offline_raises_connection_error(self):
        self.app.network_status = "offline"
        with self.assertRaises(ConnectionError):
            self.app.apply_promo_code(100000, "GIAM10")

    def test_new_os_promo_is_valid_on_os_15(self):
        self.assertEqual(self.app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_new_os_promo_raises_value_error_on_os_14(self):
        self.app.os_version = 14
        with self.assertRaises(ValueError):
            self.app.apply_promo_code(100000, "NEW_OS_ONLY")

    def test_unknown_promo_code_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.app.apply_promo_code(100000, "NOT_A_PROMO")


class TestHardLevel(unittest.TestCase):
    """Restaurant lookup tests with the GPS hardware dependency mocked."""

    def setUp(self):
        self.app = YummyApp()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_location_in_restaurant_area(self, mock_get_location):
        mock_get_location.return_value = (10.0, 105.0)
        self.assertEqual(
            self.app.get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_get_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_location_outside_restaurant_area(self, mock_get_location):
        mock_get_location.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])
        mock_get_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_lost_gps_signal_returns_location_error(self, mock_get_location):
        mock_get_location.side_effect = gps_service.GPSSignalLostError
        self.assertEqual(
            self.app.get_nearby_restaurants(),
            "Unable to determine location.",
        )
        mock_get_location.assert_called_once_with()


class TestGpsService(unittest.TestCase):
    """Tests for the default simulated hardware service."""

    def test_default_location(self):
        self.assertEqual(gps_service.get_current_location(), (10.0, 105.0))


if __name__ == "__main__":
    unittest.main()
