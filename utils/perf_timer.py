import time


# Helper function to round a non-integer number to a set number of decimal places
def roundf(num: float, places: int) -> float:
    return round(num * 10**places) / 10**places


# A utility class for keeping track of the elapsed times of various tasks
class PerfTimer:
    def __init__(self, default_precision: int = 3):
        self.init_time = 0
        self.default_precision = default_precision


    def reset(self) -> None:
        self.init_time = time.time()


    def print_elapsed_time_and_reset(self, task_name) -> None:
        elapsed_time = time.time() - self.init_time
        rounded_time = roundf(elapsed_time, self.default_precision)

        print(f'    Elapsed time for "{task_name}": {rounded_time}')
        self.reset()
