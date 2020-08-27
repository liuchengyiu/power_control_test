import psutil

def average_frequence(average_standard):
    cpu_freq = psutil.cpu_freq()[0]
    if cpu_freq < average_standard:
        return {
            "flag": False,
            "message": "平均CPU {}MHZ!".format(cpu_freq)
        }
    return {
        "flag": True,
        "message": "平均CPU {}MHZ!".format(cpu_freq)
    }
    
def single_frequence(single_standard):
    cpu_freq = psutil.cpu_freq(percpu=True);
    index = 0;
    result = [];
    for i in range(0, len(cpu_freq)):
        if cpu_freq[i][0] < single_standard:
            result.append({
                "flag": False,
                "message": str(i) + " CPU {}MHZ!".format(cpu_freq[i][0])
            })
            continue;
        result.append({
            "flag": True,
            "message": str(i) + " CPU性能 {}MHZ!".format(cpu_freq[i][0])
        })
    return result;

def cpu_frequence(d):
    result = [];
    result.append(average_frequence(d["average"]));
    result.extend(single_frequence(d["single"]));
    return result;