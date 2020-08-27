from .ram import ram_stress
from .cpu import cpu_stress
from time import sleep

def stress_test(test_array):
    test_list = [];
    for test in test_array:
        if test["type"] == "cpu":
            test_list.append({
                "func": cpu_stress,
                "param": test["param"]
            })
        if test["type"] == "ram":
            test_list.append({
                "func": ram_stress,
                "param": test["param"]
            })
    result = []
    for test in test_list:
        result.extend(test["func"](test["param"]));
        sleep(3);
    return result;