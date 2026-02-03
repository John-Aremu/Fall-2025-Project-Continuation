# mock_opm.py

class Opm:
    def __init__(self, dev_id=None, avg_count=10):
        self.dev_id = dev_id
        self.avg_count = avg_count

    def read_power(self):
        # Return a fake power value for testing GUI
        return 1.234  # dummy value in Watts

    def get_status(self):
        return {
            "id": self.dev_id or "MOCK_OPM",
            "power": self.read_power()
        }
