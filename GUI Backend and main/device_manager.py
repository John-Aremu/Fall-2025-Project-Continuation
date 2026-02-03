# device_manager.py
# Try to import real devices; fall back to mocks
try:
    from voa import Voa
except ImportError:
    from mock_voa import Voa

try:
    from optical_switch import Switch
except ImportError:
    from mock_switch import Switch


# Try to import the real OPM; fall back to dummy if unavailable
try:
    from opm import Opm
except ImportError:
    from mock_opm import Opm


class DeviceManager:
    def __init__(self):
        self.voa = None
        self.optical_switch = None
        self.opm = None

    # ---------- VOA ----------
    def connect_voa(self, device_path=None):
        self.voa = Voa(device_path)

    def set_voa_attenuation(self, attenuation_db):
        if self.voa is None:
            raise RuntimeError("VOA not connected")
        self.voa.attenuate(attenuation_db)

    def get_voa_attenuation(self):
        if self.voa is None:
            raise RuntimeError("VOA not connected")
        return self.voa.get_attenuation()

    # ---------- Optical Switch ----------
    def connect_optical_switch(self, device_path=None, num_channels=4):
        self.optical_switch = Switch(device_path, num_channels)

    def set_switch_channel(self, channel):
        if self.optical_switch is None:
            raise RuntimeError("Optical switch not connected")
        self.optical_switch.select_channel(channel)

    def get_switch_channel(self):
        if self.optical_switch is None:
            raise RuntimeError("Optical switch not connected")
        return self.optical_switch.current_chan

    # ---------- Optical Power Meter ----------
    def connect_opm(self, device_id=None, avg_count=10):
        if Opm is None:
            print("Warning: OPM not available, using dummy mode")
        self.opm = Opm(device_id, avg_count)

    def read_optical_power(self):
        if self.opm is None:
            raise RuntimeError("OPM not connected")
        return self.opm.read_power()

    # ---------- Shutdown ----------
    def close_all(self):
        if self.voa:
            self.voa.close()
        if self.optical_switch:
            self.optical_switch.ser.close()
        if self.opm and hasattr(self.opm, "resource_manager") and self.opm.resource_manager:
            self.opm.resource_manager.close()
