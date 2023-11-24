import time
import weakref
from memory_profiler import profile
import cProfile
import pstats


class RegularClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class SlotClass:
    __slots__ = ("a", "b")
    
    def __init__(self, a, b):
        self.a = a
        self.b = b


class WeakRefClass:
    def __init__(self, a, b):
        self.a = weakref.ref(a)
        self.b = weakref.ref(b)


class MockClass1:
    pass


class MockClass2:
    pass


@profile
def creating_instances(cls):
    number_of_instances = 100_000
    instances = [cls(MockClass1(), MockClass2()) for _ in range(number_of_instances)]
    return instances


@profile
def reading_attributes(instances):
    for instance in instances:
        a = instance.a
        b = instance.b


@profile
def changing_attributes(instances):
    for instance in instances:
        instance.a = MockClass1
        instance.b = MockClass2


def estimate_time(func, *args, **kwargs):
    start_ts = time.time()
    result = func(*args, **kwargs)
    end_ts = time.time()
    return result, end_ts - start_ts


def evaluate_performance(cls):
    print(f"Testing {cls.__name__} ...")
    instances, create_time  = estimate_time(creating_instances, cls)
    _, read_time = estimate_time(reading_attributes, instances)
    _, change_time = estimate_time(changing_attributes, instances)
    print(f"Creation time {cls.__name__} : {create_time}")
    print(f"Read time {cls.__name__} : {read_time}")
    print(f"Change time {cls.__name__} : {change_time}\n")


def main():
    evaluate_performance(RegularClass)
    evaluate_performance(SlotClass)
    evaluate_performance(WeakRefClass)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats()
