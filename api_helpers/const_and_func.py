import time


def check_response(code, correct_code, resp_text=None):
    error = f"Неправильный код ответа {code} != {correct_code}\n"
    if resp_text:
        error = error + f"Текст ошибки: \n {resp_text}"
    assert code == correct_code, error

def wait_while(func, timeout=30):
    """ Ждет пока переданная функция не вернет True, либо сработает таймаут """
    start_time = time.time()
    while True:
        if func():
            return True
        if (time.time() - start_time) < timeout:
            time.sleep(1)
            continue
        return False

