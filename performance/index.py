from .ram import ram_speed
from .emmc import emmc_speed
from .cpu import cpu_frequence
from time import sleep
def performance_test(test_array):
    test_list = [];
    for test in test_array:
        if test["type"] == "cpu":
            test_list.append({
                "func": cpu_frequence,
                "param": test["param"]
            })
        if test["type"] == "ram":
            test_list.append({
                "func": ram_speed,
                "param": test["param"]
            })
        if test["type"] == "emmc":
            test_list.append({
                "func": emmc_speed,
                "param": test["param"]
            })
    result = []
    for test in test_list:
        result.extend(test["func"](test["param"]));
        sleep(3);
    return result;