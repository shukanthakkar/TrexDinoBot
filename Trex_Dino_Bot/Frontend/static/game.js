// Get the game canvas element
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

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
document.addEventListener('DOMContentLoaded', function() {
    // Get reference to the sliders-container
    var slidersContainer = document.querySelector('.slider-container');
    
    // Define the number of sliders you want
    var numSliders = 5;
    
    // Loop to create and append sliders
    for (var i = 1; i <= numSliders; i++) {
        var slider = document.createElement('input');
        slider.setAttribute('type', 'range');
        slider.setAttribute('id', 'slider' + i);
        slider.setAttribute('min', '1');
        slider.setAttribute('max', '100');
        slider.setAttribute('value', '50'); // Default value
        slidersContainer.appendChild(slider);
    }
});

// Get the game canvas element
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Other game-related JavaScript code goes here...

document.addEventListener('DOMContentLoaded', function() {
    // Get reference to the sliders-container
    var slidersContainer = document.querySelector('.slider-container');

    // Define the number of sliders you want
    var numSliders = 5;

    // Loop to create and append sliders
    for (var i = 1; i <= numSliders; i++) {
        var slider = document.createElement('input');
        slider.setAttribute('type', 'range');
        slider.setAttribute('id', 'slider' + i);
        slider.setAttribute('min', '1');
        slider.setAttribute('max', '100');
        slider.setAttribute('value', '50'); // Default value
        slidersContainer.appendChild(slider);

        // Add event listener to update slider value dynamically on mousemove
        slider.addEventListener('mousemove', function(event) {
            var sliderValue = event.target.value;
            event.target.setAttribute('value', sliderValue);

            // Here, you can perform any additional actions you want when hovering over the slider
            // For example, you can update the game based on the slider value
            console.log('Slider ' + event.target.id + ' value changed to: ' + sliderValue);
        });

        // Add event listener to update slider value dynamically on input
        slider.addEventListener('input', function(event) {
            var sliderValue = event.target.value;
            event.target.setAttribute('value', sliderValue);

            // Here, you can perform any additional actions you want when slider value changes
            // For example, you can update the game based on the slider value
            console.log('Slider ' + event.target.id + ' value changed to: ' + sliderValue);
        });
    }
});

// Add event listeners to buttons
document.getElementById('startButton').addEventListener('click', startGame);
document.getElementById('stopButton').addEventListener('click', stopGame);
document.getElementById('aiButton').addEventListener('click', enableAI);
