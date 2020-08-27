from lib import run_shell

def cpu_stress(d):
    shell_str = '../bin/stress -c 1 -t {}'
    result_str = run_shell(shell_str.format(str(d['time'])))
    
    result = [{
        "flag": True,
        "message": "CPU stress pass!"
    }]
    if result.find('completed') == -1:
        result[0]['flag'] = False
        result[0]['message'] = "CPU stress failed!"
    
    return result