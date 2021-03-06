import sys
import os
import json
from test import test
from menu import menu
from record import record
from time import sleep
from test.lib import mqtt_up
def main(filename):
    json_data = {}
    hardware = []
    performance = []
    stress = []
    result = []
    print(
        '\033[1;32m \t*********************************** \033[0m\n'
        '\033[1;32m \t     please make sure test dev not used \033[0m\n'
        '\033[1;32m \t*********************************** \033[0m'
    )
    print(
        '\033[1;32m \t*********************************** \033[0m\n'
        '\033[1;32m \t     start parse config file       \033[0m\n'
        '\033[1;32m \t*********************************** \033[0m'
    )
    try:
        with open(filename, "r") as fp:
            json_data = json.load(fp)
    except OSError as e:
            print(
                '\033[1;31m \t*********************************** \033[0m\n'
                '\033[1;31m \t     parse config file failed       \033[0m\n'
                '\033[1;31m \t*********************************** \033[0m\n'
            )
            return
    print(
        '\033[1;32m \t***********************************\033[0m\n'
        '\033[1;32m \t     parse config file successful\033[0m\n'
        '\033[1;32m \t***********************************\033[0m\n'
    )
    json_data = menu(json_data)
    if json_data == False:
        print(
            '\033[1;31m exit test\033[0m\n'
        )
        return
    for key in json_data:
        if key == 'Stress_Test':
            stress = json_data[key]
        if key == 'Performance_Test':
            performance = json_data[key]
        if key == 'Hardware_Test':
            hardware = json_data[key]
    print('\033[1;32mtests is:')
    for key in json_data:
        print('{}:'.format(key))
        for item in json_data[key]:
            print('\t{}'.format(item['type']))
    print('\033[0m')
    print(
        '\033[1;32m \t***********************************\033[0m\n'
        '\033[1;32m \t     start test                     \033[0m\n'
        '\033[1;32m \t***********************************\033[0m\n'
    )
    test_tuple = ([], 0)

    test_tuple = test(performance, 'performance', test_tuple[1], 25);
    result.extend(test_tuple[0]);

    test_tuple = test(stress, 'stress', test_tuple[1], 50);
    result.extend(test_tuple[0]);

    test_tuple = test(hardware, 'hardware', test_tuple[1], 75)
    result.extend(test_tuple[0]);

    mqtt_up('test/lcd/request', 100, 9, '')
    for joins in result:
        if joins.get('flag') == False:
            mqtt_up('test/lcd/request', 75, 9, '')
            sleep(2)
            break;

    #print(result)
    record(result)
    return

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("please give config file")
    else :
        main(sys.argv[1])
    print('1111')
    sys.exit(1)