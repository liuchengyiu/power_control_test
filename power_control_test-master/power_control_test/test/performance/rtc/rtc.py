from time import sleep
from test.lib import run_shell

def shell_date(d, shell_str):
    datetime_one = run_shell(shell_str)
    print('datetime' + datetime_one)
    datetime_one = datetime_one[17:19]
    print('datetime' + datetime_one)
    sleep(d['time']-1)
    datetime_two = run_shell(shell_str)
    print('datetime' + datetime_two)
    datetime_two = datetime_two[17:19]
    print('datetime' + datetime_two)
    return datetime_one, datetime_two

def rtc_time(d):
    shell_str = 'hwclock -r'
    result = [{
        "flag": True,
        "message": "RTC datetime pass!"
    }]
    datetime= shell_date(d, shell_str)
    try:
        for a in range(1,10):
            if int(datetime[0]) + int(d['time']) > 60:
                datetime = shell_date(d, shell_str)
            else:
                break
        if int(datetime[1]) - int(datetime[0]) != int(d['time']):
            result[0]['flag'] = False
            result[0]['message'] = "RTC datetime failed!"
    except Exception as e:
        result[0]['flag'] = False
        result[0]['message'] = "RTC datetime failed!"
    return result


