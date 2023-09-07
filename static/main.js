document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    // Function to draw a point
    function drawPoint(x, y, color) {
        context.fillStyle = color;
        context.beginPath();
        context.arc(x * canvas.width, y * canvas.height, 3, 0, 2 * Math.PI);
        context.fill();
    }

    // Update the values on the page
    function updateValues() {
        const xDiv = document.getElementById('x');
        const yDiv = document.getElementById('y');
        const colorDiv = document.getElementById('color');

        xDiv.textContent = `X: ${canvas_data.x.toFixed(2)}`;
        yDiv.textContent = `Y: ${canvas_data.y.toFixed(2)}`;
        colorDiv.textContent = `Color: ${canvas_data.color}`;
    }

    // Request updates every second
    setInterval(updateValues, 1000);
});

// Fetch data from the server
fetch('/demo')
    .then(response => response.text())
    .then(data => console.log(data));
