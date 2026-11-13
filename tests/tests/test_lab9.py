import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from smart_auditor import (
    BulkDiscount,
    DigitalProduct,
    Inventory,
    NoDiscount,
    Order,
    OrderLine,
    PercentageDiscount,
    PhysicalProduct,
    ProductFactory,
    StudentDiscount,
    Supplier,
    load_products,
)


class TestLab9DesignPatternsAndValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S01", "Test Supplier", "test@supplier.com")
        self.p1 = ProductFactory.create("physical", "P01", "Laptop", 100.0, 10, self.supplier, 2.0)
        self.p2 = ProductFactory.create("digital", "D01", "IDE License", 50.0, 20, self.supplier, 150.0)

    def test_strategy_discounts(self):
        order = Order("ORD-100")
        order.add_order_line(self.p1, 2)  # 200.0
        order.add_order_line(self.p2, 1)  # 50.0 -> Total = 250.0

        self.assertAlmostEqual(order.calculate_total(), 250.0)

        order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

        order.set_discount(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_factory_creation_and_unknown_type(self):
        self.assertIsInstance(self.p1, PhysicalProduct)
        self.assertIsInstance(self.p2, DigitalProduct)
        with self.assertRaises(ValueError):
            ProductFactory.create("service", "S01", "Setup", 30.0, 5, self.supplier)

    def test_domain_validation(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P99", "Bad Price", 0.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D99", "Bad Stock", 10.0, -1, self.supplier)
        with self.assertRaises(ValueError):
            OrderLine(self.p1, 0)

    def test_csv_loader_skips_bad_rows_and_handles_missing_file(self):
        inv = Inventory()
        if os.path.exists("products.csv"):
            loaded = load_products("products.csv", inv, self.supplier)
            self.assertEqual(loaded, 3)
            self.assertEqual(len(inv.products), 3)

        missing_loaded = load_products("nonexistent_file.csv", inv, self.supplier)
        self.assertEqual(missing_loaded, 0)


if __name__ == "__main__":
    unittest.main()