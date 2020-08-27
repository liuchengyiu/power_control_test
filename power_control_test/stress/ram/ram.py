from lib import run_shell

def ram_stress(d):
    shell_str = '../bin/stress -vm {} --vm-bytes {} --vm-hang {} --timeout {}'
    result_str = run_shell(
                    shell_str.format(str(d['num'],
                    str(d['size']),
                    str(d['release_time']),
                    str(d['last_time']),
                ))

    result = [{
        "flag": True,
        "message": "ram stress pass!"
    }]
    if result.find('completed') == -1:
        result[0]['flag'] = False
        result[0]['message'] = "ram stress failed!"
    
    return result