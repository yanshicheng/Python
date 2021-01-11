from apps import app

import time

@app.task()
def ans_playbook(val):
    print(val)
    time.sleep(2)
    print('d')
    return 'ok'