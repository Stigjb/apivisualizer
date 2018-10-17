from flask import Flask, render_template, request, jsonify

from apivisualizer.highestproduct import highest_product

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')


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
