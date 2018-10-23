/// <reference path='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.js' />
/* global Chart */

Object.assign(Chart.defaults.global.elements.line, { tension: 0.2, fill: false });
Chart.defaults.global.title.display = true;
Chart.defaults.global.maintainAspectRatio = false;

const colors = ['#73d216', '#3465a4', '#cc0000'];
const thresholds = {
  'PM2.5': 25,
  PM10: 50,
  NO2: 100,
};

function getPointStyle(threshold) {
  return value => value < threshold ? 'circle' : 'crossRot';
}

function getPointRadius(threshold) {
  return value => value < threshold ? 3 : 6;
}

function checkResponseOK(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response.json();
}

function displayError(message) {
  document.getElementById('error-msg').innerHTML = message;
}

function hideError() {
  displayError('');
}

const makeChart = (ctx, xs, ys) => {
  const colorIter = colors.values();
  const datasets = ys.map((component) => {
    const label = component.component;
    const data = component.values;
    const color = colorIter.next().value;
    const pointStyle = data.map(getPointStyle(thresholds[label]));
    const pointRadius = data.map(getPointRadius(thresholds[label]));
    return {
      label,
      data,
      pointStyle,
      pointRadius,
      borderColor: color,
      backgroundColor: color,
    };
  });
  if (window.airQualityChart === undefined) {
    window.airQualityChart = new Chart(ctx, {
      type: 'line',
      options: {
        scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'µg/m³',
            },
          }],
        },
      },
    });
  }
  window.airQualityChart.config.data = {
    labels: xs,
    datasets,
  };
  const stationName = document.getElementById('station-select').value;
  window.airQualityChart.config.options.title.text = `Målestasjon: ${stationName}`;
  window.airQualityChart.update();
  return window.airQualityChart;
};

function submitNiluForm() {
  const body = new FormData(document.getElementById('nilu-form'));
  fetch('/_nilu_form', { method: 'POST', body })
    .then(checkResponseOK)
    .then((result) => {
      if (result.error !== undefined) {
        throw Error(result.error);
      }
      return result;
    })
    .then((result) => {
      const ctx = document.getElementById('chart').getContext('2d');
      return makeChart(ctx, result.xs, result.ys);
    })
    .then((res) => {
      hideError();
      return res;
    })
    .catch(err => displayError(`Could not generate chart. Reason: ${err.message}`));
}

function initDateForm() {
  const now = new Date();
  now.setDate(now.getDate() - 1); // No data for today yet
  const endDateString = now.toISOString().slice(0, 10);
  now.setDate(now.getDate() - 7); // One week back
  const startDateString = now.toISOString().slice(0, 10);
  document.getElementById('startDate').value = startDateString;
  document.getElementById('endDate').value = endDateString;
}

async function initStations() {
  const body = new FormData();
  body.append('area', 'Oslo');
  return fetch('/_nilu_stations', { method: 'POST', body })
    .then(checkResponseOK)
    .then((result) => {
      const select = document.getElementById('station-select');
      select.innerHTML = '';
      result.stations.forEach((element) => {
        const opt = document.createElement('option');
        opt.value = element;
        opt.innerHTML = element;
        select.appendChild(opt);
      });
      hideError();
    })
    .catch(err => displayError(`Could not initialize station list. Reason: ${err.message}`));
}

window.onload = async () => {
  initDateForm();
  await initStations();
  submitNiluForm();
};
