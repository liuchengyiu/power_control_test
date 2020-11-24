from test.lib import run_shell

def deal_shell(shell_str):
    if shell_str.find("/s") == -1:
        return -1

    for line in shell_str.split("\r\n"):
        unit = 1
        if line.find("copied") == -1:
            continue
        speed = float(line[line.rfind(",")+1: line.find("/s")-2].strip())
        if line.find("MB") > 0:
            unit = 1000
        if line.find("KB") > 0 or line.find("kB") > 0:
            unit = 1000000
        speed = speed / unit
        return speed

def size_shell(shell_str : str):
    if shell_str.find('Mem') == -1:
        return -1

    shell_str = shell_str.replace(' ', '')
    size = float(shell_str[shell_str.find('Mem:')+4 : shell_str.find('G')])
    return size

def emmc_speed(d):
    result = []
    standard = d["speed"]
    best_size = d["size"]
    shell_result = run_shell("dd if=/dev/zero of=file bs=1M count=1024")
    run_shell("sudo rm -rf file")
    speed = deal_shell(shell_result)
    if speed == -1:
        result.append({
            "flag": False,
            "message": "Emmc speed test failed"
        })
    if speed < standard:
        result.append({
            "flag": False,
            "message": "Emmc speed is {} GB/s".format(str(speed))
        })
    if speed >= standard:
        result.append({
            "flag": True,
            "message": "Emmc speed is {} GB/s".format(str(speed))
        })

    shell_result = run_shell("free -h")
    size = size_shell(shell_result)
    if size == -1:
        result.append({
            "flag": False,
            "message": "Emmc size query fails"
        })
    if best_size-0.2 > size or best_size+0.2 < size:
        result.append({
            "flag": False,
            "message": "Emmc size is {} GB".format(str(size))
        })
    else:
        result.append({
            "flag": True,
            "message": "Emmc size is {} GB".format(str(size))
        })
    return result