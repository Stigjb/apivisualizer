import datetime as dt

from flask import Flask, render_template, request, jsonify, redirect
from requests.exceptions import HTTPError

from apivisualizer.highestproduct import highest_product
from apivisualizer.nilu import get_daily_mean, get_stations

app = Flask(__name__)


def date_from_isoformat(isostr):
    return dt.datetime.strptime(isostr, '%Y-%m-%d').date()


@app.route('/')
def index():
    return redirect('/luftkvalitet')


@app.route('/luftkvalitet')
def luftkvalitet():
    return render_template('luftkvalitet.html')


@app.route('/highest_product')
def highest_product_page():
    return render_template('product.html')


@app.route('/_highest_product', methods=['POST'])
def _highest_product():
    raw_nums = request.form['numbers']
    nums = []
    for num in raw_nums.split():
        try:
            nums.append(int(num))
        except ValueError:
            return jsonify(error="%s is not a valid integer" % num)
    try:
        prod = highest_product(nums)
    except ValueError:
        return jsonify(error="Needs at least three integers")
    return jsonify(result=prod)


@app.route('/_nilu_form', methods=['POST'])
def _nilu_form():
    station = request.form['station']
    components = request.form.getlist('component[]')
    start_date = date_from_isoformat(request.form['startDate'])
    end_date = date_from_isoformat(request.form['endDate'])
    end_date += dt.timedelta(days=1)
    if end_date - start_date > dt.timedelta(days=30):
        return jsonify(error="Maximum length of time period is 30 days")
    try:
        result = get_daily_mean(start_date, end_date, station, components)
    except (ValueError, HTTPError) as err:
        return jsonify(error=str(err))
    if not result['ys']:
        return jsonify(error='No data found for query')

    return jsonify(xs=result['xs'], ys=result['ys'])


@app.route('/_nilu_stations', methods=['POST'])
def _nilu_stations():
    try:
        area = request.form['area']
        return jsonify(stations=get_stations(area))
    except HTTPError as e:
        print("Error from NILU's API: %s" % str(e))
        # Return a hard coded list of stations when the API is down
        return jsonify(stations=[
            'Manglerud',
            'Kirkeveien',
            'Breivoll',
            'Bygdøy Alle',
            'Sofienbergparken',
            'Hjortnes',
            'Aker Sykehus'
        ])


if __name__ == '__main__':
    app.run()
