from time import time, sleep


class PrplLogger:
    def __init__(self, file):
        self.id = file
    def log(self, message, status='info', record: bool = True):
        match status.lower():
            case 'info':
                print(f'\33[44m{self.id} - {round(time())} INFO:\33[0m {message}')
            case 'error':
                print(f'\33[43m{self.id} - {round(time())} ERROR:\33[0m {message}')
            case 'warning':
                print(f'\33[41m{self.id} - {round(time())} WARNING:\33[0m {message}')
            case 'critical':
                print(f'\33[45m{self.id} - {round(time())} CRITICAL:\33[0m {message}')
            case _:
                print(f'{self.id} - {round(time())} ELSE: {message}')
        if record:
            with open(f'logs/{self.id}.log', 'a', encoding="utf-8") as f:
                f.write(f'{self.id} - {round(time())} {status.upper()}: {message}\n')


if __name__ == "__main__":
    l = PrplLogger('logger')
    l.log('This is a test message')
    sleep(1)
    l.log('This is an error message', 'error')
    sleep(1)
    l.log('This is a warning message', 'warning')
    sleep(1)
    l.log('This is a critical message', 'critical')
    