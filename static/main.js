document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const xValue = document.getElementById('xValue');
    const yValue = document.getElementById('yValue');
    const colorValue = document.getElementById('colorValue');
    const demoButton = document.getElementById('demoButton');

    function drawPoint(x, y, color) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x * canvas.width, y * canvas.height, 5, 0, Math.PI * 2);
        ctx.fill();
    }

    function updateValues(x, y, color) {
        xValue.textContent = x.toFixed(2);
        yValue.textContent = y.toFixed(2);
        colorValue.textContent = color;
    }

    demoButton.addEventListener('click', function () {
        const randomX = Math.random();
        const randomY = Math.random();
        const randomColor = getRandomColor();
        
        drawPoint(randomX, randomY, randomColor);
        updateValues(randomX, randomY, randomColor);

        // Send the data to the server
        fetch('/draw_point', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ x: randomX, y: randomY, color: randomColor }),
        })
            .then(response => response.json())
            .then(data => console.log(data));
    });

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
});
