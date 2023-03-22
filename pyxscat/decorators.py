import functools
import time
from datetime import datetime
import matplotlib.pyplot as plt
from other_functions import messages
import random

def count(func):
    @functools.wraps(func)
    def wrapper_count(*args, **kwargs):
        count += 1
        return func(*args, **kwargs)
    count = 0
    return wrapper_count

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        st = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        run_time = end - st
        print(f'The process has lasted {run_time:.2f} seconds.\n')
        return value
    return wrapper_timer

def st_end_message(st_msg, end_msg):
    def decorator_end_message(func):
        @functools.wraps(func)
        def wrapper_end_message(*args, **kwargs):
            print(f'{st_msg} \nTime: {datetime.now()}\n')
            value = func(*args, **kwargs)
            print(f'{end_msg} \nTime: {datetime.now()}\n')
            return value
        return wrapper_end_message
    return decorator_end_message

def clear_plt(func):
    @functools.wraps(func)
    def wrapper_clear_plt(*args, **kwargs):
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        from IPython.display import clear_output
        clear_output(wait=True)
        return func(*args, **kwargs)
    return wrapper_clear_plt

def random_message(func):
    @functools.wraps(func)
    def wrapper_random_message(*args, **kwargs):
        len_msgs = len(messages)
        rand_n = random.randrange(0, len_msgs)
        value = func(*args, **kwargs)
        print(messages[rand_n])
        return value
    return wrapper_random_message

def try_or_continue(error_message):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                print(f'Error in {func.__name__}: {error_message}')
        return wrapper
    return decorator