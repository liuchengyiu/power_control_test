from test.lib import run_shell

def ram_speed(d):
    standard = d["speed"]
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
    return results
