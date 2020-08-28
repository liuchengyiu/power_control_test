import sys
import os
import json
from test import test
def main(filename):
    json_data = {}
    hardware = []
    performance = []
    stress = []
    result = []
    print('\033[1;32m \t*********************************** \033[0m')
    print('\033[1;32m \t     start parse config file       \033[0m')
    print('\033[1;32m \t*********************************** \033[0m')
    try:
        with open(filename, "r") as fp:
            json_data = json.load(fp)
    except OSError as e:
            print('\033[1;31m \t*********************************** \033[0m')
            print('\033[1;31m \t     parse config file failed       \033[0m')
            print('\033[1;31m \t*********************************** \033[0m')
            return 
    for key in json_data:
        if key == "Stress_Test":
            stress = json_data[key]
        if key == "Performance_Test":
            performance = json_data[key]
        if key == "Hardware_Test":
            hardware = json_data[key]
    print('\033[1;32m \t*********************************** \033[0m')
    print('\033[1;32m \t     parse config file successful  \033[0m')
    print('\033[1;32m \t*********************************** \033[0m')   
    print('\033[1;32m \t     start test                     \033[0m')
    print('\033[1;32m \t*********************************** \033[0m')    
    result.extend(test(performance, 'performance'));
    result.extend(test(hardware, 'hardware'))
    result.extend(test(stress, 'stress'))
    print(result)
    return

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("please give config file")
    else :
        main(sys.argv[1])