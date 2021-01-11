from apps import app

import time

@app.task()
def ans_command(val):
    print(val)
    time.sleep(4)
    print('任务执行完成')
    return 'ok'