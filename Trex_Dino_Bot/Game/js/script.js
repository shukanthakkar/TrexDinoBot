/*
const width = 600;
const height = 200;
// Function to fetch and parse CSV file
async function fetchCSV(url) {
    const response = await fetch(url);
    return response.text();
}

// Function to load and display assets
async function loadAndDisplayAssets() {
    const frameInfoDiv = document.getElementById('frameInfo');
    const assetsContainer = document.getElementById('assetsContainer');

    // Fetch CSV data
    const csvData = await fetchCSV('assets/images/resources.csv');

    // Parse CSV data
    const rows = csvData.trim().split('\n');
    rows.shift(); // Remove header row

    rows.forEach(rowText => {
        const [assetName, , X1, Y1, X2, Y2] = rowText.split(',');
        if (assetName === 'ground') {
            // Ground asset
            const assetDiv = document.createElement('div');
            assetDiv.className = 'asset';
            assetDiv.innerHTML = `
                <p>${assetName}</p>
                <div style="width: ${width}px; height: ${Y2 - Y1}px; overflow: hidden;position:absolute;left:0px;top:150px">
                    <img id="${assetName}" src="assets/images/resources.png" alt="${assetName}" style="margin-left: -${X1}px; margin-top: -${Y1}px;">
                    <img id="${assetName}1" src="assets/images/resources.png" alt="${assetName}1" style="margin-left: -${X1}px; margin-top: -${Y1}px;">
                </div>
            `;
            assetsContainer.appendChild(assetDiv);                       
            
            } else {
            // Other assets
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = X2 - X1;
                canvas.height = Y2 - Y1;
                ctx.drawImage(img, X1, Y1, X2 - X1, Y2 - Y1, 0, 0, canvas.width, canvas.height);

                const resizedCanvas = document.createElement('canvas');
                const resizedCtx = resizedCanvas.getContext('2d');
                resizedCanvas.width = canvas.width / 2;
                resizedCanvas.height = canvas.height / 2;
                resizedCtx.drawImage(canvas, 0, 0, canvas.width, canvas.height, 0, 0, resizedCanvas.width, resizedCanvas.height);

                const resizedImage = new Image();
                resizedImage.src = resizedCanvas.toDataURL();
                resizedImage.alt = assetName;

                const assetDiv = document.createElement('div');
                assetDiv.className = 'asset';
                assetDiv.appendChild(resizedImage);
                assetsContainer.appendChild(assetDiv);
            };
            img.src = 'assets/images/resources.png';
        }
    });

    // Rotate ground image
    const ground = document.getElementById('ground');
    const ground1 = document.getElementById('ground1');    
    if (ground) {
        let position = 0;
        let frameCount = 0;
        setInterval(() => {
            position -= 1;
            ground.style.left = `${position}px`;
            ground1.style.left = `${position+width}px`;            
            if (position <= -600) {
                position = 0;
            }
            frameCount++;
            frameInfoDiv.textContent = `Frame Number: ${frameCount}, Frame Rate: ${Math.round(1000 / 16)} fps`; // 16ms is approximately 60fps
        }, 16);
    }
}

// Call the function to load and display assets
loadAndDisplayAssets();
*/
const width = 600;
const height = 200;

// Function to fetch and parse CSV file
async function fetchCSV(url) {
    const response = await fetch(url);
    return response.text();
}

// Function to load and display assets
async function loadAndDisplayAssets() {
    const frameInfoDiv = document.getElementById('frameInfo');
    const assetsContainer = document.getElementById('assetsContainer');

    // Fetch CSV data
    const csvData = await fetchCSV('assets/images/resources.csv');

    // Parse CSV data
    const rows = csvData.trim().split('\n');
    rows.shift(); // Remove header row

    rows.forEach(rowText => {
        const [assetName, , X1, Y1, X2, Y2] = rowText.split(',');
        if (assetName === 'ground') {
            // Ground asset
            const assetDiv = document.createElement('div');
            assetDiv.className = 'asset';
            assetDiv.innerHTML = `
                <p>${assetName}</p>
                <div style="width: ${width}px; height: ${Y2 - Y1}px; overflow: hidden; position: relative;">
                    <img id="${assetName}" src="assets/images/resources.png" alt="${assetName}" style="margin-left: -${X1}px; margin-top: -${Y1}px;">
                    <img id="${assetName}1" src="assets/images/resources.png" alt="${assetName}1" style="margin-left: -${X1}px; margin-top: -${Y1}px;">
                </div>
            `;
            assetsContainer.appendChild(assetDiv);
        } else {
            // Other assets
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = X2 - X1;
                canvas.height = Y2 - Y1;
                ctx.drawImage(img, X1, Y1, X2 - X1, Y2 - Y1, 0, 0, canvas.width, canvas.height);

                const resizedCanvas = document.createElement('canvas');
                const resizedCtx = resizedCanvas.getContext('2d');
                resizedCanvas.width = canvas.width / 2;
                resizedCanvas.height = canvas.height / 2;
                resizedCtx.drawImage(canvas, 0, 0, canvas.width, canvas.height, 0, 0, resizedCanvas.width, resizedCanvas.height);

                const resizedImage = new Image();
                resizedImage.src = resizedCanvas.toDataURL();
                resizedImage.alt = assetName;

                const assetDiv = document.createElement('div');
                assetDiv.className = 'asset';
                assetDiv.appendChild(resizedImage);
                assetsContainer.appendChild(assetDiv);
            };
            img.src = 'assets/images/resources.png';
        }
    });

    // Rotate ground image
    const ground = document.getElementById('ground');
    const ground1 = document.getElementById('ground1');

    if (ground && ground1) {
        let position = 0;
        let frameCount = 0;
        setInterval(() => {
            position -= 1;
            ground.style.left = `${position}px`;
            ground1.style.left = `${position + 600}px`;
            if (position <= -width) {
                position = 0;
            }
            frameCount++;
            frameInfoDiv.textContent = `Frame Number: ${frameCount}, Frame Rate: ${Math.round(1000 / 16)} fps`; // 16ms is approximately 60fps
        }, 16);
    }
}

// Call the function to load and display assets
loadAndDisplayAssets();
