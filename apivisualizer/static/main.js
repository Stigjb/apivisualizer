window.onload = () => {
    const resultDiv = document.getElementById("result");

    formAction = () => {
        resultDiv.innerHTML = "Calculating result ..."
        const body = new FormData(document.getElementById("numbers-input"));
        fetch('/_highest_product', {method: 'POST', body })
            .then(response => {
                if (!response.ok) {
                    throw Error(response.statusText);
                }
                return response.json();
            })
            .then(result => { 
                if (result.result !== undefined) {
                    resultDiv.innerHTML = result.result;
                } else {
                    resultDiv.innerHTML = result.error;
                }
            })
            .catch(reason => { resultDiv.innerHTML = reason });
    }
}
