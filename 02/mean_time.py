import time


def mean(last_k_calls):
    if not isinstance(last_k_calls, int):
        raise TypeError("last_k_calls must be an integer")
    if last_k_calls <= 0:
        raise ValueError("last_k_calls must be a positive integer")

    def decorated(func):
        call_durations = []

        def inner(*args, **kwargs):
            start_ts = time.time()
            result = func(*args, **kwargs)
            end_ts = time.time()
            call_duration = end_ts - start_ts
            call_durations.append(call_duration)
            if len(call_durations) > last_k_calls:
                call_durations.pop(0)
            if len(call_durations) <= last_k_calls:
                mean_call_duration = sum(call_durations) / len(call_durations)
                print(
                    f"Mean time of last {last_k_calls} calls: {mean_call_duration:.9f} seconds"
                )
            return result

        return inner

    return decorated


def foo(arg1):
    return arg1
