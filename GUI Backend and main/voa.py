import serial
import sys

class Voa:
    VERBOSE = True
    dev = None
    ser = None

    def __init__(self, dev_path):
        self.ser = serial.Serial(port=dev_path, baudrate=115200, bytesize=8, parity="N", stopbits=1)
        if self.VERBOSE:
            print("VOA: connecting..")
        id = self.get_id()
        att = self.get_attenuation()
        if self.VERBOSE:
            print("VOA ID: %s" % id)
            print("VOA current attenuation: %.2f" % att)
        
    def get_id(self):
        self.ser.write(b'ID?\n')
        id = self.ser.read_until(expected=b"\n")
        # if VERBOSE:
        #     print("VOA ID: %s" % id)
        return id

    def get_attenuation(self):
        resp = None

        while resp is None or "ERR" in resp:
            self.ser.write(b"A1 A?\n")
            resp = self.ser.read_until(expected=b"\n")
            resp = resp.decode("utf-8")

        att = float(resp)
        return att

    def attenuate(self, attenuation_db):
        att_str = "%.2f" % attenuation_db
        print("VOA: setting attenuation to %sdB" % att_str)
        self.ser.write(('A1 A %s\n' % att_str).encode("utf-8"))
        resp = self.ser.read_until(expected=b"\n")

        while resp != b"OK\n":
            print("VOA: attenuator busy.. retrying..")
            self.ser.write(('A1 A %s\n' % att_str).encode("utf-8"))
            resp = self.ser.read_until(expected=b"\n")
        
        print("VOA: attenuation setting done")

    def close(self):
        self.ser.close()

if __name__ == "__main__":
    voa = Voa("/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DP04LVOF-if00-port0")

    if len(sys.argv) > 1:
        att = float(sys.argv[1])
        voa.attenuate(att)

    # get_id()
