function toggleRanges() {
    const inputRanges = document.getElementById('inputRanges');
    inputRanges.classList.toggle('show'); 

    if (inputRanges.classList.contains('show')) {
        inputRanges.style.maxHeight = inputRanges.scrollHeight + "px";
    } else {
        inputRanges.style.maxHeight = "0";
    }
}



function submitData() {
    const temperature = parseFloat(document.getElementById('temperature').value);
    const windSpeed = parseFloat(document.getElementById('windSpeed').value);
    const fuelMoisture = parseFloat(document.getElementById('fuelMoisture').value);
    const duffMoisture = parseFloat(document.getElementById('duffMoisture').value);
    const initialSpread = parseFloat(document.getElementById('initialSpread').value);
    
    const data = {
        temperature: temperature,
        windSpeed: windSpeed,
        fuelmoisturecode: fuelMoisture,
        duffmoisturecode: duffMoisture,
        initialspreadindex: initialSpread
    };

    console.log("Sending data to Python:", data);

    window.pywebview.api.handle_request(data).then(result => {

        if(result.toFixed(4) < 40){
            var a = "The probability of a wildfire occurring is VERY LOW based on the current conditions"
        }
        else if(result.toFixed(4) >= 40 && result.toFixed(4) <= 55) {
            var a = "The probability of a wildfire occurring is MODERATE based on the current conditions"
        }
        else if(result.toFixed(4) >= 55){
            var a = "The probability of a wildfire occurring is HIGH based on the current conditions"
        }

        document.getElementById('dataOutput').innerText = a;  
        
        const outputElement = document.getElementById('output');
        outputElement.classList.add('show'); 
        console.log("Received prediction result:", result.toFixed(4));
    }).catch(err => {
        console.error('Error:', err);
    });
}
