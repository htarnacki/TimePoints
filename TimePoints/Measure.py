import time
from typing import List, Dict, Any, Tuple


_measurements = {}
_formats = {}
_default_format = 'Duration of "{name_range}": {humanized_duration}'


def set_format(format: str) -> None:
    if not isinstance(format, str):
        raise TypeError('Format should be of type "str"')
    global _default_format
    _default_format = format


def _humanize_duration(duration: float) -> str:
    days = int(duration // (24 * 3600))
    duration = duration % (24 * 3600)
    hours = int(duration // 3600)
    duration %= 3600
    minutes = int(duration // 60)
    duration %= 60
    seconds = round(duration, 2)
    parts_a = []
    parts_b = []
    if days == 1:
        parts_a.append('1 day')
    elif days > 1:
        parts_a.append(f'{days} days')
    if hours == 1:
        parts_a.append('1 hour')
    elif hours > 1:
        parts_a.append(f'{days} hours')
    if minutes == 1:
        parts_a.append('1 minute')
    elif minutes > 1:
        parts_a.append(f'{minutes} minutes')
    if seconds == 1:
        parts_b.append('1 second')
    else:
        parts_b.append(f'{seconds} seconds')
    if len(parts_a) > 0:
        parts_a = [', '.join(parts_a)]
    string = ' and '.join(parts_a + parts_b)
    return string


def _calculate_average_for_time_points(time_points: List[float]) -> float:
    average = 0.0
    if len(time_points) > 1:
        for idx in range(1, len(time_points)):
            duration = time_points[idx] - time_points[idx - 1]
            average += duration
        average = average / (len(time_points) - 1)
    return average


class Measurement():

    def __init__(self, name: str) -> None:
        self.name = name
        self._compare_to_index = -2

    def _calculate_idx_a_b(self) -> Tuple[float, float]:
        if self._compare_to_index < 0:
            idx_a = len(self.time_points) + self._compare_to_index
        else:
            idx_a = self._compare_to_index
        idx_a = min(len(self.time_points) - 1, idx_a)
        idx_a = max(idx_a, 0)
        idx_b = len(self.time_points) - 1
        return (idx_a, idx_b)

    @property
    def time_points(self) -> List[float]:
        return _measurements[self.name]

    @property
    def duration(self) -> float:
        idx_a, idx_b = self._calculate_idx_a_b()
        return self.time_points[idx_b] - self.time_points[idx_a]

    def __getitem__(self, idx: int) -> 'Measurement':
        if not isinstance(idx, int):
            raise TypeError(f'{idx} should be of type "int"')
        measurement = Measurement(self.name)
        measurement._compare_to_index = idx
        return measurement

    def __call__(self, format=None, **kwargs: Dict[str, Any]) -> 'Measurement':
        print(self.to_string(format=format, **kwargs))
        return self

    def __repr__(self) -> str:
        a = self.time_points[0]
        b = self.time_points[-1]
        return f'<{self.name}: {a}->{b}>'

    def to_string(self, format: str = None, **kwargs: Dict[str, Any]) -> str:
        if format is None:
            if self.name in _formats.keys():
                format = _formats[self.name]
            else:
                format = _default_format
        idx_a, idx_b = self._calculate_idx_a_b()
        # a = self.time_points[idx_a]
        # b = self.time_points[idx_b]
        # duration = b - a
        hduration = _humanize_duration(self.duration)
        string = format \
            .replace('{name}', self.name) \
            .replace(
                '{name_range}',
                f'{self.name}[{idx_a}]->{self.name}[{idx_b}]') \
            .replace('{duration}', str(self.duration)) \
            .replace('{humanized_duration}', hduration) \
            .replace('{hduration}', hduration) \
            .replace('{idx_a}', str(idx_a)) \
            .replace('{idx_b}', str(idx_b))
        for key, value in kwargs.items():
            string = string.replace(f'{{{key}}}', str(value))
        return string

    def __str__(self) -> str:
        return self.to_string()

    def set_format(self, format: str = None) -> 'Measurement':
        if format is None:
            if self.name in _formats.keys():
                del _formats[self.name]
        else:
            _formats[self.name] = format
        return self

    def squeeze(self) -> 'Measurement':
        global _measurements
        time_points = _measurements[self.name]
        if len(time_points) > 2:
            time_points = [
                time_points[0],
                time_points[-1]
            ]
            _measurements[self.name] = time_points
        return self

    def summary(self) -> 'Measurement':
        from rich.console import Console
        from rich.table import Table
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Measurement", style="dim")
        table.add_column("Points count", justify="right")
        table.add_column("Average duration", justify="right")
        table.add_column("First point", justify="right")
        table.add_column("Last point", justify="right")
        table.add_row(
            self.name,
            str(len(self.time_points)),
            _humanize_duration(
                _calculate_average_for_time_points(self.time_points)),
            str(self.time_points[0]),
            str(self.time_points[-1])
        )
        console.print(table)
        return self


def __getattr__(attr: str):
    if attr not in _measurements.keys():
        _measurements[attr] = []
    _measurements[attr].append(time.perf_counter())
    return Measurement(attr)


def delete(measurement: str) -> None:
    if measurement in _measurements.keys():
        del _measurements[measurement]
    if measurement in _formats.keys():
        del _formats[measurement]


def clear() -> None:
    global _measurements
    global _formats
    global _default_format
    _measurements = {}
    _formats = {}
    _default_format = 'Duration of "{name_range}": {humanized_duration}'


def summary() -> None:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Measurement", style="dim")
    table.add_column("Points count", justify="right")
    table.add_column("Average duration", justify="right")
    table.add_column("First point", justify="right")
    table.add_column("Last point", justify="right")
    for measurement, time_points in _measurements.items():
        table.add_row(
            measurement,
            str(len(time_points)),
            _humanize_duration(
                _calculate_average_for_time_points(time_points)),
            str(time_points[0]),
            str(time_points[-1])
        )
    console.print(table)
