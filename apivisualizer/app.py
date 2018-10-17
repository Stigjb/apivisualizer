import datetime as dt

from flask import Flask, render_template, request, jsonify

from apivisualizer.highestproduct import highest_product
from apivisualizer.nilu import get_daily_mean

app = Flask(__name__)


def _date_range(start_date: dt.date, end_date: dt.date):
    next_date = start_date
    while next_date < end_date:
        yield next_date
        next_date = next_date + dt.timedelta(days=1)


@app.route('/')
def hello_world():
    return render_template('product.html')


@app.route('/luftkvalitet')
def luftkvalitet():
    station = 'Manglerud'
    component = 'PM10'
    start_date = dt.date(2018, 10, 1)
    end_date = dt.date(2018, 10, 15)

    results = get_daily_mean(start_date, end_date, station, [component])
    observations = []
    for date, value in zip(_date_range(start_date, end_date), results[component]):
        observations.append({
            "date": date.isoformat(),
            "value": value
        })
    return render_template(
        'luftkvalitet.html',
        station=station,
        component=component,
        observations=observations)


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


if __name__ == '__main__':
    app.run()
