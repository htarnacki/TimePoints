# TimePoints

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Easly save and collect different, dynamic time points in your application and print durations between any of them.


### Install with pip

```bash
$ pip install TimePoints
$ pip install TimePoints[reports]  # if you want to use "summary" functionality
```

### Usage

```python
>>> import time
>>> from TimePoints import Measure
>>> Measure.sleep  # point 0
>>> time.sleep(1)
>>> Measure.sleep()  # point 1
Duration of "sleep[0]->sleep[1]": 1 second

>>> import time
>>> from TimePoints import Measure
>>> sleep = Measure.sleep  # point 0
>>> time.sleep(1)
>>> Measure.sleep  # point 1
>>> print(str(sleep.duration))
1.0011622839956544

>>> import time
>>> from TimePoints import Measure
>>> sleep = Measure.sleep  # point 0
>>> time.sleep(1)
>>> Measure.sleep  # point 1
>>> time.sleep(1.5)
>>> Measure.sleep  # point 2
>>> print(str(sleep[0].duration))
>>> time.sleep(1)
>>> print(str(Measure.sleep[0].duration))  # point 3
2.5062046920002103
3.5122546620302118

>>> import time
>>> from TimePoints import Measure
>>> some_operation_stats = Measure.some_operation  # point 0
>>> time.sleep(1)
>>> Measure.some_operation  # point 1
>>> time.sleep(1)
>>> Measure.some_operation  # point 2
>>> some_operation_stats.summary()
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Measurement    ┃ Points count ┃ Average duration ┃      First point ┃       Last point ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ some_operation │            3 │         1 second │ 133321.685088924 │ 133323.687620218 │
└────────────────┴──────────────┴──────────────────┴──────────────────┴──────────────────┘

>>> import time
>>> from TimePoints import Measure
>>> Measure.Building  # point 0 of "Building"
>>> time.sleep(2)
>>> Measure.Building(format='{name} last: {humanized_duration}')  # point 1 of "Building"
>>> Measure.Deploying  # point 0 of "Deploying"
>>> time.sleep(1)
>>> Measure.Deploying(format='{name} last: {humanized_duration}')  # point 1 of "Deploying"
>>> Measure.summary()
Building last: 2.0 seconds
Deploying last: 1 second
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Measurement ┃ Points count ┃ Average duration ┃      First point ┃       Last point ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Building    │            2 │      2.0 seconds │ 133067.569995202 │ 133069.571433436 │
│ Deploying   │            2 │         1 second │ 133069.571682702 │ 133070.572820608 │
└─────────────┴──────────────┴──────────────────┴──────────────────┴──────────────────┘

>>> import time
>>> from TimePoints import Measure
>>> some_operation_stats = Measure.some_operation  # point 0
>>> time.sleep(1)
>>> Measure.some_operation  # point 1
>>> time.sleep(1)
>>> Measure.some_operation  # point 2
>>> time.sleep(1)
>>> Measure.some_operation  # point 3
>>> some_operation_stats[0](format='Duration of {name} from point 0: {hduration}')
>>> some_operation_stats[1](format='Duration of {name} from point 1: {hduration}')
>>> some_operation_stats[2](format='Duration of {name} from point 2: {hduration}')
Duration of some_operation from point 0: 3.0 seconds
Duration of some_operation from point 1: 2.0 seconds
Duration of some_operation from point 2: 1 second

>>> import time
>>> from TimePoints import Measure
>>> for i in range(5):
>>>     Measure.loop()
>>>     time.sleep(1)
Duration of "loop[0]->loop[0]": 0.0 seconds
Duration of "loop[0]->loop[1]": 1 second
Duration of "loop[1]->loop[2]": 1 second
Duration of "loop[2]->loop[3]": 1 second
Duration of "loop[3]->loop[4]": 1 second

>>> import time
>>> from TimePoints import Measure
>>> for i in range(5):
>>>     Measure.loop()
>>>     time.sleep(1)
>>> Measure.loop[0]()
Duration of "loop[0]->loop[0]": 0.0 seconds
Duration of "loop[0]->loop[1]": 1 second
Duration of "loop[1]->loop[2]": 1 second
Duration of "loop[2]->loop[3]": 1 second
Duration of "loop[3]->loop[4]": 1 second
Duration of "loop[0]->loop[5]": 5.01 seconds

>>> import time
>>> from TimePoints import Measure
>>> for i in range(5):
>>>     Measure.loop
>>>     time.sleep(1)
>>> for i in range(5):
>>>     Measure.loop2
>>>     time.sleep(1)
>>> Measure.summary()
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Measurement ┃ Points count ┃ Average duration ┃      First point ┃       Last point ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ loop        │            5 │         1 second │ 133960.331337131 │ 133964.334118174 │
│ loop2       │            5 │         1 second │ 133965.335290972 │ 133969.338710931 │
└─────────────┴──────────────┴──────────────────┴──────────────────┴──────────────────┘

>>> import time
>>> from TimePoints import Measure
>>> for i in range(5):
>>>     Measure.loop
>>>     time.sleep(1)
>>> Measure.loop.summary().squeeze().summary()
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Measurement ┃ Points count ┃ Average duration ┃      First point ┃     Last point ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ loop        │            6 │         1 second │ 135384.873706028 │ 135389.8791503 │
└─────────────┴──────────────┴──────────────────┴──────────────────┴────────────────┘
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Measurement ┃ Points count ┃ Average duration ┃      First point ┃     Last point ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ loop        │            2 │     5.01 seconds │ 135384.873706028 │ 135389.8791503 │
└─────────────┴──────────────┴──────────────────┴──────────────────┴────────────────┘
```

### Custom formatting placeholders:
- `name`: name of a measurement eg. "a"
- `name_range`: name of a measurement followed by time point comparison range eg. "a[992]->a[993]"
- `duration`: duration beetween last measured time point and the one set as current comparison point eg. "0.36081594599818345"
- `humanized_duration`: humanized duration beetween last measured time point and the one set as current comparison point eg. "6 minutes and 47.53 seconds"
- `hduration`: the same as `humanized_duration`
- `idx_a`: integer number of index for time point against which we make a comparison
- `idx_b`: integer number of index for last time point

For example:

```python
# Return string representation of this measurement with one time custom formatting
>>> import time
>>> from logging import warning
>>> from TimePoints import Measure
>>> Measure.a
>>> time.sleep(1)
>>> warning(Measure.a.to_string(format='Why "{name}" took so long: {hduration}!'))
WARNING:root:Why "a" took so long: 1 second!

# Print this measurement with one time custom formatting
>>> import time
>>> from TimePoints import Measure
>>> Measure.building
>>> time.sleep(1)
>>> Measure.building(format='How long was the {name} process: {hduration}')
How long was the building process: 1 second

# Set custom formatting for one measurement
>>> import time
>>> from TimePoints import Measure
>>> Measure.building.set_format(format='How long was the {name} process: {hduration}')
>>> time.sleep(1)
>>> Measure.building()
>>> time.sleep(1)
>>> Measure.building()
How long was the building process: 1 second
How long was the building process: 1 second

# Set custom formatting globally
>>> import time
>>> from TimePoints import Measure
>>> Measure.set_format(format='How long was the {name} process: {hduration}')
>>> Measure.building
>>> time.sleep(1)
>>> Measure.building()
>>> Measure.deploying
>>> time.sleep(1)
>>> Measure.deploying()
How long was the building process: 1 second
How long was the deploying process: 1 second

# Pass additional dynamic args to custom formatting
>>> import time
>>> from TimePoints import Measure
>>> Measure.set_format(format='Stage {stage_number} of {name} process: {hduration}')
>>> Measure.building
>>> time.sleep(1)
>>> Measure.building(stage_number=1)
>>> time.sleep(1)
>>> Measure.building(stage_number=2)
Stage 1 of building process: 1 second
Stage 2 of building process: 1 second
```

### Other APIs:
- `Measure.delete('a')` -> delete 'a' measurement
- `Measure.clear()` -> clear all measurements
