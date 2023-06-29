
SERVER_ADDRESS = '91.222.238.238'
BASE_URL = f'http://{SERVER_ADDRESS}:3003'


def check_response(code, correct_code, resp_text=None):
    error = f"Неправильный код ответа {code} != {correct_code}\n"
    if resp_text:
        error = error + f"Текст ошибки: \n {resp_text}"
    assert code == correct_code, error


