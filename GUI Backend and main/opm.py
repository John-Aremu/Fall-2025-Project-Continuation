import pyvisa
from ThorlabsPM100 import ThorlabsPM100
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import sys

class Opm:
    
    resource_manager = None
    power_meter = None

    def __init__(self, dev_id, avg_count=10):
        self.resource_manager = pyvisa.ResourceManager()
        inst = self.resource_manager.open_resource(dev_id, read_termination='\n')

        # self.resource_manager.list_resources()
        # inst = rm.open_resource('USB0::0x1313::0x8076::M00819707::0::INSTR', read_termination='\n') # OPM 1
        #inst = rm.open_resource('USB0::4883::32886::M01071376::0::INSTR', read_termination='\n') # OPM 2
        #inst = rm.open_resource('USB0::4883::32886::M01071372::0::INSTR', read_termination='\n') # OPM 3 (bottom box)
        
        inst.query("*IDN?")
        self.power_meter = ThorlabsPM100(inst=inst)

        print("Configuring OPM")
        print("    Set average count to: ", avg_count)
        self.power_meter.sense.average.count = avg_count
        self.power_meter.sense.power.dc.range.auto = "ON"
        self.power_meter.sense.correction.wavelength = 850

        print("    Measurement type :", self.power_meter.getconfigure)
        print("    Wavelength       :", self.power_meter.sense.correction.wavelength)

    def disconnect(self):
        self.resource_manager.close()

    # executes one measurement, returns power in mW
    def measure_once_mw(self):
        return self.power_meter.read * 1000.0
        
    def mw_to_dbm(self, mw_value):
        if mw_value < 1/10000:
            return -99.0
        else:
            return 10*math.log(mw_value, 10)

    # executes multiple measurements (num_iterations), and returns the average result, units are dBm
    def measure(self, num_iterations=50, sleep=0):
        powers = np.empty(num_iterations, dtype=np.float64)
        for i in range(num_iterations):
            powers[i] = self.measure_once_mw()
        # avg_power_mw = powers.mean()
        avg_power_mw = np.median(powers)
        return self.mw_to_dbm(avg_power_mw)

if __name__ == '__main__': 
    ids = ["USB0::0x1313::0x8076::M01217675::0::INSTR",  # OPM 1
           "USB0::4883::32886::M01071376::0::INSTR",     # OPM 2
           "USB0::10c4::ea60::M01217675::0::INSTR"]     # OPM 3

    if len(sys.argv) < 2:
        print("Usage: opm.py <OPM_INDEX> [num_iterations]")
        sys.exit()
        
    num_iterations = 50
    if len(sys.argv) > 2:
        num_iterations = int(sys.argv[2])

    opm_idx = ids[int(sys.argv[1])]
    opm = Opm(opm_idx)
    power = opm.measure(num_iterations=num_iterations)
    print("Mean power: %.2f dBm" % power)





