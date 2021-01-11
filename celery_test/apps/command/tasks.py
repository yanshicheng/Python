from apps import app

import time

@app.task()
def command(val):
    print(val)
    time.sleep(5)
    print('定时任务')
    return 'ok'