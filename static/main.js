document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const drawBtn = document.getElementById('drawBtn');
    const xInput = document.getElementById('x');
    const yInput = document.getElementById('y');
    const colorInput = document.getElementById('color');
    const pointList = document.getElementById('pointList');

    drawBtn.addEventListener('click', function () {
        const x = parseFloat(xInput.value);
        const y = parseFloat(yInput.value);
        const color = colorInput.value;

        // Ensure x and y are within the canvas boundaries
        if (x >= 0 && x <= 1 && y >= 0 && y <= 1) {
            // Draw the point on the canvas
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(x * canvas.width, y * canvas.height, 5, 0, Math.PI * 2);
            ctx.fill();

            // Add the point to the list
            const pointItem = document.createElement('li');
            pointItem.style.color = color;
            pointItem.textContent = `(${x}, ${y})`;
            pointList.appendChild(pointItem);

            // Clear input values
            xInput.value = '';
            yInput.value = '';
            colorInput.value = '';
        } else {
            alert('Please enter valid coordinates (0.0 - 1.0) for X and Y.');
        }
    });
});
