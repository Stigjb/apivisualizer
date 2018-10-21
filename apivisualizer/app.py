import datetime as dt

from flask import Flask, render_template, request, jsonify

from apivisualizer.highestproduct import highest_product
from apivisualizer.nilu import get_daily_mean, get_stations

app = Flask(__name__)


def date_from_isoformat(isostr):
    return dt.datetime.strptime(isostr, '%Y-%m-%d').date()


@app.route('/')
def hello_world():
    return render_template('product.html')


@app.route('/luftkvalitet')
def luftkvalitet():
    return render_template('luftkvalitet.html')


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
    print(request.form)
    station = request.form['station']
    components = request.form.getlist('component[]')
    start_date = date_from_isoformat(request.form['startDate'])
    end_date = date_from_isoformat(request.form['endDate'])
    end_date += dt.timedelta(days=1)

    try:
        result = get_daily_mean(start_date, end_date, station, components)
    except ValueError as err:
        return str(err), 400
    if not result['ys']:
        return 'No data found for query', 204

    return jsonify(xs=result['xs'], ys=result['ys'])


@app.route('/_nilu_stations', methods=['POST'])
def _nilu_stations():
    area = request.form['area']
    return jsonify(stations=get_stations(area))


if __name__ == '__main__':
    app.run()
