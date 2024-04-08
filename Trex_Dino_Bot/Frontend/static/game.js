// Get the game canvas element
    const canvas = document.getElementById('gameCanvas');
   // const ctx = canvas.getContext('2d');

// Variables to track Dino position and movement
let dinoX = 10;
let dinoY = 80;
let isJumping = false;
let jumpHeight = 10;
let gravity = 1.2;

// Function to draw the Dino character
function drawDino() {
    ctx.fillStyle = 'black';
    ctx.fillRect(dinoX, dinoY, 44, 44); // Adjust width and height as needed
}

// Function to update the game state
function update() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the Dino character
    drawDino();

    // Apply gravity when Dino is not jumping
    if (!isJumping && dinoY < 80) {
        dinoY += gravity;
    }

    // Handle jumping
    if (isJumping) {
        dinoY -= jumpHeight;
        jumpHeight -= 0.5; // Adjust the jump height decrement as needed

        // If Dino reaches the ground, stop jumping
        if (dinoY >= 80) {
            isJumping = false;
            jumpHeight = 10; // Reset jump height for next jump
        }
    }

    // Request animation frame for smooth animation
    requestAnimationFrame(update);
}

// Function to handle keydown events
function onKeyDown(event) {
    if (event.keyCode === 32) { // Space key
        // Start jumping if Dino is not already jumping
        if (!isJumping) {
            isJumping = true;
        }
    }
}

// Add event listener for keydown events
document.addEventListener('keydown', onKeyDown);

// JavaScript code for handling game interactions
// You'll need to implement the necessary functionality here to interact with the game canvas

// Function to start the game
function startGame() {
    // Your code to start the game
    update(); // Start the game loop
}

// Function to stop the game
function stopGame() {
    // Your code to stop the game
    // Stop the animation loop by not requesting a new frame
}

// Function to enable AI mode
function enableAI() {
    // Your code to enable AI mode
    // Implement AI logic here
}



    //making the slider dynamic
// Get all slider elements
    // Get all slider elements
const sliders = document.querySelectorAll('.slider-container input[type="range"]');

// Add event listener to each slider
sliders.forEach(slider => {
    slider.addEventListener('input', () => { // Use input event for real-time updating
        updateSliderValue(slider);
    });

    slider.addEventListener('mousemove', () => { // Add mousemove event for hover effect
        showSliderValue(slider);
    });
});


// Function to update the displayed value of the slider
function updateSliderValue(slider) {
    const valueDisplay = slider.parentElement.querySelector('.value-display'); // Get the element to display the value
    if (valueDisplay) {
        const value = slider.value; // Get the current value of the slider
        valueDisplay.innerText = value; // Update the displayed value
    }
}

// Function to show the value of the slider on hover
function showSliderValue(slider) {
    const valueDisplay = slider.parentElement.querySelector('.value-display'); // Get the element to display the value
    if (valueDisplay) {
        const value = slider.value; // Get the current value of the slider
        valueDisplay.innerText = value; // Update the displayed value
        valueDisplay.style.display = 'block'; // Show the value
    }
}

// Function to hide the value of the slider when not hovering
function hideSliderValue(slider) {
    const valueDisplay = slider.parentElement.querySelector('.value-display'); // Get the element to display the value
    if (valueDisplay) {
        valueDisplay.style.display = 'none'; // Hide the value
    }
}






// Add event listeners to buttons
//document.getElementById('startButton').addEventListener('click', startGame);
//document.getElementById('stopButton').addEventListener('click', stopGame);
//document.getElementById('aiButton').addEventListener('click', enableAI);
