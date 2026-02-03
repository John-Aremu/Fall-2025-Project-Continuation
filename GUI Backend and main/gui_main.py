# gui_main.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QTabWidget, QSlider, QHBoxLayout, QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt
from device_manager import DeviceManager


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Backend
        self.dm = DeviceManager()

        # Connect devices (dummy OPM works automatically)
        self.dm.connect_opm("dummy_id")
        # For testing, you can also connect dummy VOA/Switch if you add mocks
        # self.dm.connect_voa("dummy_voa_path")
        # self.dm.connect_optical_switch("dummy_switch_path", num_channels=4)

        # Window setup
        self.setWindowTitle("ATCA Test Stand GUI")
        self.resize(500, 400)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.voa_tab(), "VOA")
        self.tabs.addTab(self.switch_tab(), "Optical Switch")
        self.tabs.addTab(self.opm_tab(), "OPM")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    # ----------------- VOA Tab -----------------
    def voa_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.voa_label = QLabel("VOA Attenuation: -- dB")
        layout.addWidget(self.voa_label)

        # Slider for VOA attenuation
        self.voa_slider = QSlider(Qt.Orientation.Horizontal)
        self.voa_slider.setMinimum(0)
        self.voa_slider.setMaximum(30)  # adjust range as needed
        self.voa_slider.setTickInterval(1)
        self.voa_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        layout.addWidget(self.voa_slider)

        # Set button
        set_button = QPushButton("Set Attenuation")
        set_button.clicked.connect(self.set_voa_attenuation)
        layout.addWidget(set_button)

        tab.setLayout(layout)
        return tab

    def set_voa_attenuation(self):
        value = self.voa_slider.value()
        try:
            self.dm.set_voa_attenuation(value)
            self.voa_label.setText(f"VOA Attenuation: {value} dB")
        except Exception as e:
            self.voa_label.setText(f"Error: {e}")

    # ----------------- Optical Switch Tab -----------------
    def switch_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select channel:"))

        # Combo box for channels (example 1-4)
        self.channel_selector = QComboBox()
        self.channel_selector.addItems([str(i) for i in range(1, 5)])
        layout.addWidget(self.channel_selector)

        set_channel_btn = QPushButton("Set Channel")
        set_channel_btn.clicked.connect(self.set_switch_channel)
        layout.addWidget(set_channel_btn)

        self.switch_label = QLabel("Current channel: --")
        layout.addWidget(self.switch_label)

        tab.setLayout(layout)
        return tab

    def set_switch_channel(self):
        channel = int(self.channel_selector.currentText())
        try:
            self.dm.set_switch_channel(channel)
            self.switch_label.setText(f"Current channel: {channel}")
        except Exception as e:
            self.switch_label.setText(f"Error: {e}")

    # ----------------- OPM Tab -----------------
    def opm_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.power_label = QLabel("Current Power: -- W")
        layout.addWidget(self.power_label)

        # Dummy/real indicator
        self.opm_mode_label = QLabel("")
        layout.addWidget(self.opm_mode_label)
        self.update_opm_mode()

        # Read power button
        read_button = QPushButton("Read Power")
        read_button.clicked.connect(self.read_power)
        layout.addWidget(read_button)

        tab.setLayout(layout)
        return tab

    def update_opm_mode(self):
        if self.dm.opm.__class__.__module__ == "mock_opm":
            self.opm_mode_label.setText("OPM: Dummy Mode")
        else:
            self.opm_mode_label.setText("OPM: Real Device")

    def read_power(self):
        try:
            power = self.dm.read_optical_power()
            if self.dm.opm.__class__.__module__ == "mock_opm":
                self.power_label.setText(f"OPM: Dummy Mode, Power: {power} W")
            else:
                self.power_label.setText(f"OPM: Real Device, Power: {power} W")
        except Exception as e:
            self.power_label.setText(f"Error: {e}")


# ----------------- Run the app -----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
