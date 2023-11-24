
#### Testing RegularClass ...
| ncalls  | tottime | percall | cumtime | percall | filename:lineno(function)                          |
|---------|---------|---------|---------|---------|----------------------------------------------------|
|       3 |   0.000 |   0.000 |  23.107 |   7.702 | weakref_slots_regular.py:57(estimate_time)         |
|       3 |   0.000 |   0.000 |  23.107 |   7.702 | memory_profiler.py:1185(wrapper)                   |
|       3 |   0.000 |   0.000 |  23.106 |   7.702 | memory_profiler.py:759(f)                          |
|       1 |   9.730 |   9.730 |   9.730 |   9.730 | weakref_slots_regular.py:43(reading_attributes)    |
|       1 |   9.706 |   9.706 |   9.706 |   9.706 | weakref_slots_regular.py:50(changing_attributes)   |
|       1 |   0.000 |   0.000 |   3.670 |   3.670 | weakref_slots_regular.py:36(creating_instances)    |
|       1 |   3.538 |   3.538 |   3.670 |   3.670 | weakref_slots_regular.py:39(<listcomp>)            |
| 100000  |   0.132 |   0.000 |   0.132 |   0.000 | weakref_slots_regular.py:9(init)               |
|     ... |   ...   |   ...   |   ...   |   ...   | ...                                                |
Profile: RegularClass Execution Time

#### Testing SlotClass ...
| ncalls  | tottime | percall | cumtime | percall | filename:lineno(function)                          |
|---------|---------|---------|---------|---------|----------------------------------------------------|
|       3 |   0.000 |   0.000 |  23.566 |   7.855 | weakref_slots_regular.py:57(estimate_time)         |
|       3 |   0.000 |   0.000 |  23.566 |   7.855 | memory_profiler.py:1185(wrapper)                   |
|       3 |   0.000 |   0.000 |  23.564 |   7.855 | memory_profiler.py:759(f)                          |
|       1 |  10.363 |  10.363 |  10.363 |  10.363 | weakref_slots_regular.py:50(changing_attributes)   |
|       1 |   9.628 |   9.628 |   9.628 |   9.628 | weakref_slots_regular.py:43(reading_attributes)    |
|       1 |   0.000 |   0.000 |   3.573 |   3.573 | weakref_slots_regular.py:36(creating_instances)    |
| 100000  |   0.119 |   0.000 |   0.119 |   0.000 | weakref_slots_regular.py:17(init)              |
|     ... |   ...   |   ...   |   ...   |   ...   | ...                                                |
Profile: SlotClass Execution Time

#### Testing WeakRefClass ...
| ncalls  | tottime | percall | cumtime | percall | filename:lineno(function)                          |
|---------|---------|---------|---------|---------|----------------------------------------------------|
|       3 |   0.000 |   0.000 |  24.345 |   8.115 | weakref_slots_regular.py:57(estimate_time)         |
|       3 |   0.000 |   0.000 |  24.345 |   8.115 | memory_profiler.py:1185(wrapper)                   |
|       3 |   0.000 |   0.000 |  24.343 |   8.114 | memory_profiler.py:759(f)                          |
|       1 |  10.143 |  10.143 |  10.143 |  10.143 | weakref_slots_regular.py:43(reading_attributes)    |
|       1 |  10.137 |  10.137 |  10.137 |  10.137 | weakref_slots_regular.py:50(changing_attributes)   |
|       1 |   0.000 |   0.000 |   4.063 |   4.063 | weakref_slots_regular.py:36(creating_instances)    |
| 100000  |   0.168 |   0.000 |   0.168 |   0.000 | weakref_slots_regular.py:23(init)              |
|     ... |   ...   |   ...   |   ...   |   ...   | ...                                                |
Profile: WeakRefClass Execution Time

Note: The output has been condensed with ellipsis (...) to indicate that the table is truncated and contains more entries.