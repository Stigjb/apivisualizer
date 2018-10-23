import requests
import datetime as dt
from typing import Optional, Dict, Iterable

BASE_URL = "https://api.nilu.no"
ISO_DATEFMT = "%Y-%m-%dT%H:%M:%S"


def _fetch_data(path: str, params: Optional[Dict[str, str]] = None):
    response = requests.get(BASE_URL + path, params=params)
    response.raise_for_status()
    return response.json()


def is_recent(time_str: str):
    """Whether the timestamp is within the last day."""
    time_str = time_str[:19]  # Strip off time zone offset
    timestamp = dt.datetime.strptime(time_str, ISO_DATEFMT)
    return dt.datetime.now() - timestamp < dt.timedelta(days=1)


def get_areas():
    data = _fetch_data("/lookup/areas")
    return [record['area'] for record in data]


def get_components():
    data = _fetch_data("/lookup/components")
    return [record['component'] for record in data]


def get_stations(area: Optional[str] = None):
    params = None
    if area is not None:
        params = {'area': area}
    data = _fetch_data("/lookup/stations", params=params)
    return [
        record['station'] for record in data
        if is_recent(record['lastMeasurment'])
    ]


def _date_range(start_date: dt.date, end_date: dt.date):
    next_date = start_date
    while next_date < end_date:
        yield next_date
        next_date = next_date + dt.timedelta(days=1)


def get_daily_mean(start_date: dt.date, end_date: dt.date, station: str, components: Iterable[str]):
    if end_date <= start_date:
        raise ValueError('Start date must be before end date.')
    if not components:
        raise ValueError('At least one component must be passed.')
    params = {'components': ';'.join(components)}
    path_parts = [
        "/stats/day",
        start_date.isoformat(),
        end_date.isoformat(),
        station
    ]
    data = _fetch_data('/'.join(path_parts), params=params)
    xs = [str(d) for d in _date_range(start_date, end_date)]
    component_ys = []
    for element in data:
        component = element['component']
        ys = []
        if not element['values']:
            continue
        value_iterator = iter(element['values'])
        value = next(value_iterator)
        for date in xs:
            if value['dateTime'].startswith(date):
                ys.append(value['value'])
                try:
                    value = next(value_iterator)
                except StopIteration:
                    if len(xs) < len(ys):
                        raise ValueError('X and Y length mismatch')
                    while len(xs) > len(ys):
                        ys.append(None)
                    break
            else:
                ys.append(None)
        component_ys.append({
            'component': component,
            'values': ys
        })
    return {
        'xs': xs,
        'ys': component_ys
    }
