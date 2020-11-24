from test.lib import run_shell

def size_shell(shell_str: str):
    if shell_str.find('sda1') == -1:
        return -1
    shell_str = shell_str.replace(' ', '')
    shell_str = shell_str[shell_str.find('sda1'):]
    shell_str = shell_str[shell_str.find('sda1')+4: shell_str.find('G')]
    return float(shell_str)

def ram_speed(d):
    standard = d["speed"]
    best_size = d["size"]
    average = 0
    index = 0
    results = []
    for i in range(0, 10):
        result = run_shell("dd if=/dev/zero of=/dev/null bs=1M count=1024")
        if result.find("/s") == -1:
            results.append({
                "flag": False,
                "message": "num: " + str(i) + " ram speed test failed"
            })
            continue
        for line in result.split("\r\n"):
            unit = 1
            if line.find("copied") == -1:
                continue
            speed = float(line[line.rfind(",")+1: line.find("/s")-2].strip())
            if line.find("MB") > 0:
                unit = 1000
            if line.find("KB") > 0 or line.find("kB") > 0:
                unit = 1000000
            speed = speed / unit
            results.append({
                "flag": True,
                "message": "num: " + str(i) + " ram speed: "+str(speed) + "GB/s"
            })
            average = average + speed;
            index = index + 1
    if index == 0:
        average = 0
    else:
        average = average / index
    flag = True
    if average < standard:
        flag = False
    results.append({
        "flag": flag,
        "message": "average ram: " + str(average) + "GB/s"
    })
    size = run_shell('df -h')
    size = size_shell(size)
    if size == -1:
        results.append({
            "flag": False,
            "message": "Ram size query failed"
        })
    if size > best_size + 2 or size < best_size - 2:
        results.append({
            "flag": False,
            "message": "Ram size is {} G".format(str(size))
        })
    else:
        results.append({
            "flag": True,
            "message": "Ram size is {} G".format(str(size))
        })

    return results
