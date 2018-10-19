import requests
from datetime import date
from typing import Optional, Dict, Iterable

BASE_URL = "https://api.nilu.no"


def _fetch_data(path: str, params: Optional[Dict[str, str]] = None):
    response = requests.get(BASE_URL + path, params=params)
    return response.json()


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
    return [record['station'] for record in data]


def get_daily_mean(startdate: date, enddate: date, station: str, components: Iterable[str]):
    if enddate <= startdate:
        raise ValueError('Start date must be before end date.')
    if not components:
        raise ValueError('At least one component must passed.')
    params = {'components': ';'.join(components)}
    path_parts = [
        "/stats/day",
        startdate.isoformat(),
        enddate.isoformat(),
        station
    ]
    data = _fetch_data('/'.join(path_parts), params=params)
    return {
        record['component']: [value['value'] for value in record['values']]
        for record in data
    }
