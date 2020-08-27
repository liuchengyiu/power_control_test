import sys
import os
import json
from performance import performance_test
from hardware import hardware_test
from stress import stress_test
from lib import run_shell

def main(filename):
    json_data = {}
    hardware = []
    performance = []
    stress = []
    result = []
    try:
        with open(filename, "r") as fp:
            json_data = json.load(fp)
    except OSError as e:
        print("read file data error")
    for key in json_data:
        if key == "Stress_Test":
            stress = json_data[key]
        if key == "Performance_Test":
            performance = json_data[key]
        if key == "Hardware_Test":
            hardware = json_data[key]
    result.extend(performance_test(performance));
    result.extend(hardware_test(hardware))
    result.extend(stress_test(stress))
    print(result)
    

if __name__ == '__main__':
    print(sys.argv)
    if (len(sys.argv) < 2):
        print("please give config file")
    else :
        main(sys.argv[1])