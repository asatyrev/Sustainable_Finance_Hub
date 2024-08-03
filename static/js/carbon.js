
document.addEventListener('DOMContentLoaded', () => {
    // Get the form element and the calculate button
    const calculateButton = document.querySelector('button[type="submit"]');

    // Add event listener to the button
    calculateButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent form submission
        
        // Get values from the inputs
        const electricity = parseFloat(document.querySelector('#electricity input').value) || 0;
        const gas = parseFloat(document.querySelector('#gas input').value) || 0;
        const mileage = parseFloat(document.querySelector('#mileage input').value) || 0;
        const flights = parseFloat(document.querySelector('#flights input').value) || 0;
        const water = parseFloat(document.querySelector('#water input').value) || 0;
        const food = parseFloat(document.querySelector('#food input').value) || 0;
        
        // Define conversion factors (example values, adjust as needed)
        const electricityFactor = 0.5; // kg CO2 per dollar
        const gasFactor = 2.3; // kg CO2 per dollar
        const mileageFactor = 0.25; // kg CO2 per mile
        const flightFactor = 0.2; // kg CO2 per flight
        const waterFactor = 0.002; // kg CO2 per gallon
        const foodFactor = 0.3; // kg CO2 per dollar spent
        
        // Calculate total carbon footprint
        const totalCarbonFootprint = (electricity * electricityFactor) +
                                     (gas * gasFactor) +
                                     (mileage * mileageFactor) +
                                     (flights * flightFactor) +
                                     (water * waterFactor) +
                                     (food * foodFactor);
        
        // Display result and tips in the results section
        const resultText = document.querySelector('#result-text');
        resultText.innerHTML = `Your total carbon footprint is <strong>${totalCarbonFootprint.toFixed(2)}</strong> kg CO2.<br>${getTips(totalCarbonFootprint)}`;
    });

    // Function to provide tips based on the total carbon footprint
    function getTips(carbonFootprint) {
        if (carbonFootprint < 500) {
            return 'Great job! Your carbon footprint is below average. Continue maintaining your sustainable habits.';
        } else if (carbonFootprint < 1000) {
            return 'Good job! But there are still some areas to improve. Consider reducing your energy consumption and using public transport more often.';
        } else {
            return 'Your carbon footprint is quite high. Try to reduce your energy consumption, drive less, and minimize air travel.';
        }
    }
    
});
