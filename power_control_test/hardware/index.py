from .eth import eth_speed
from time import sleep
def hardware_test(test_array):
    test_list = [];
    for test in test_array:
        if test["type"] == "eth":
            test_list.append({
                "func": eth_speed,
                "param": test["param"]
            })
    result = []
    for test in test_list:
        result.extend(test["func"](test["param"]));
        sleep(3);
    return result