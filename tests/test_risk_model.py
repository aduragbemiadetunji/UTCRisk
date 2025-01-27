import unittest
from risk_model import RiskModel

class TestRiskModel(unittest.TestCase):
    def test_initialization(self):
        model = RiskModel()
        self.assertIsNotNone(model)

if __name__ == "__main__":
    unittest.main()
