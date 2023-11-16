import cProfile
import pstats


def profile_deco(func):
    profiler = cProfile.Profile()

    def wrapper(*args, **kwargs):
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        return result

    def print_stat():
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


if __name__ == "__main__":
    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()
    sub.print_stat()
