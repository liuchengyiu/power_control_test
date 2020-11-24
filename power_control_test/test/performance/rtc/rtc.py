from time import sleep, time
from test.lib import run_shell

def shell_date(d, shell_str):
    try:

        datetime_one = int(run_shell(shell_str)[17:19])
        time_one = int(time())
        sleep(d['time'])

        datetime_two = int(run_shell(shell_str)[17:19])
        time_two = int(time())
        print(time_one, ' ', time_two)
        print(datetime_one, ' ', datetime_two)
        if datetime_one + d['time'] > 60:
            datetime_two = 60 + datetime_two
        print(datetime_one, ' ', datetime_two)
        if datetime_two - datetime_one == d['time'] + 1:
            return True
        return False
    except Exception as e:
        return False

def rtc_time(d):
    shell_str = 'hwclock -r'
    result = [{
        "flag": True,
        "message": "RTC datetime pass!"
    }]
    try:
        for a in range(2):
            datetime = shell_date(d, shell_str)
            if datetime:
                result[0]['flag'] = True
                result[0]['message'] = "RTC datetime pass!"
                return result
        result[0]['flag'] = False
        result[0]['message'] = "RTC datetime failed!"

    except Exception as e:
        result[0]['flag'] = False
        result[0]['message'] = "RTC datetime failed"
    return result


