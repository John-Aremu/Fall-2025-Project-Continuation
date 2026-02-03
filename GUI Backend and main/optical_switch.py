import serial
import time
import sys

class Switch():

    switch_type = None
    current_chan = None
    SWITCH_SLEEP_CALIB = None
    SWITCH_SLEEP_SELECT = None

    def __init__(self, dev_path, num_of_chans):
        self.ser = serial.Serial(
                port = dev_path,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout = 1
            )

        self.switch_type = num_of_chans

        # self.select_chan(1)
    
    def select_chan(self, chan):
        if(chan <= 0):
            raise ValueError("Invalid channel passed to the switch: %d" % chan)
        
        # open the device file
        if not self.ser.is_open:
            self.ser.open()

        # select sleep time
        if self.switch_type == 8:
            SWITCH_SLEEP_CALIB = 2.0
            SWITCH_SLEEP_SELECT = 2.0
        elif self.switch_type == 32:
            SWITCH_SLEEP_CALIB = 3.0
            SWITCH_SLEEP_SELECT = 3.0
        else:
            SWITCH_SLEEP_CALIB = 5.5
            SWITCH_SLEEP_SELECT = 5.5

        # command for calibraton
        self.ser.write(bytearray([0x01, 0x20, 0x00, 0x00]))
        time.sleep(SWITCH_SLEEP_CALIB)
        # command for output channel selection
        self.ser.write(bytearray([0x01, 0x12, 0x00, chan]))
        time.sleep(SWITCH_SLEEP_SELECT)
        # self.ser.close()

        self.current_chan = chan

        return 0

    def get_current_chan(self):
        return self.current_chan

if __name__ == "__main__":
    devs = [
            ("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10MBA5M-if00-port0", 8), # RX source 1 / RX IN 1
            ("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10MBBYQ-if00-port0", 32), # RX switch 1 / RX OUT 1
            ("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10MACK4-if00-port0", 8), # RX source 2 / RX IN 2
            ("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10MACKY-if00-port0", 32), # RX switch 2 / RX OUT 2
            #("/dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_36a355733cc6ef11813076527a5e3baa-if00-port0", 64), # 1x64
            ("/dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_56c3d12f28c6ef11bec16f527a5e3baa-if00-port0",64), # 1x64
            ("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10MB6PC-if00-port0", 8) # TX dest / TX OUT
            ]

    # handle command line args
    if(len(sys.argv) < 3):
        print("INVALID ARGUMENTS, use: python3 optical_switch.py <switch_number> <chan>")
        sys.exit()

    switch_idx = int(sys.argv[1])
    switch_dev = devs[switch_idx][0]
    switch_num_of_chans = devs[switch_idx][1]
    chan = int(sys.argv[2])

    sw = Switch(switch_dev, switch_num_of_chans)
    sw.select_chan(chan)
    print(sw.get_current_chan())
