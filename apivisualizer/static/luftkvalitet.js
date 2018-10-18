/// <reference path="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.js" />

const lineDefaults = Chart.defaults.global.elements.line
lineDefaults.tension = 0.2;
lineDefaults.fill = false;

const colors = ["#4e9a06", "#204a87", "#a40000"];

const makeChart = (ctx, xs, ys) => {
    let colorIter = colors.values();
    datasets = ys.map(component => {
        let col = colorIter.next().value;
        return {
            label: component.component,
            data: component.values,
            borderColor: col,
            backgroundColor: col 
        };
    });
        
    console.log('Made new chart');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: xs,
            datasets
        }
    });
}

function submitNiluForm() {
    const body = new FormData(document.getElementById("nilu-form"));
    fetch('/_nilu_form', {method: 'POST', body })
        .then(response => {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response.json();
        })
        .then(result => { 
            const ctx = document.getElementById('chart').getContext('2d');
            console.log(result);
            makeChart(ctx, result.xs, result.ys)
            if (result.values !== undefined) {
                console.log(result.observations);
            } else {
                resultDiv.innerHTML = result.error;
            }
        })
        .catch(reason => { resultDiv.innerHTML = reason });
    }

function initDateForm() {
    let now = new Date();
    now.setDate(now.getDate() - 1) // No data for today yet
    const endDateString = now.toISOString().slice(0, 10)
    now.setDate(now.getDate() - 7) // One week back
    const startDateString = now.toISOString().slice(0, 10)
    document.getElementById('startDate').value = startDateString
    document.getElementById('endDate').value = endDateString
}

async function initStations() {
    let body = new FormData();
    body.append('area', 'Oslo');
    return fetch('/_nilu_stations', {method: 'POST', body})
        .then(response => {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response.json();
        })
        .then(result => {
            const select = document.getElementById('station-select');
            select.innerHTML = '';
            result.stations.forEach(element => {
                let opt = document.createElement('option');
                opt.value = element;
                opt.innerHTML = element;
                select.appendChild(opt);                
            });
        })
        .catch(console.log);
}

window.onload = async () => {
    initDateForm();
    await initStations();
    submitNiluForm();
}
