const canvas = document.getElementById('sudokuCanvas');
const ctx = canvas.getContext('2d');
const cellSize = 50;
let grid = Array(9).fill().map(() => Array(9).fill(0)); // 9x9 grid initialized to 0
let selectedCell = null;

// Function to draw the grid
function drawGrid() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  for (let i = 0; i <= 9; i++) {
    let thickness = i % 3 === 0 ? 3 : 1;  // Thicker lines for 3x3 grid sections
    ctx.beginPath();
    ctx.moveTo(i * cellSize, 0);
    ctx.lineTo(i * cellSize, canvas.height);
    ctx.moveTo(0, i * cellSize);
    ctx.lineTo(canvas.width, i * cellSize);
    ctx.lineWidth = thickness;
    ctx.stroke();
  }

  // Highlight the selected cell if any
  if (selectedCell) {
    ctx.fillStyle = 'rgba(173, 216, 230, 0.3)';  // Light blue
    ctx.fillRect(selectedCell.col * cellSize, selectedCell.row * cellSize, cellSize, cellSize);
  }
}

// Function to draw the numbers on the grid
function drawNumbers() {
  ctx.font = "30px Arial";
  ctx.fillStyle = 'black';

  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      if (grid[row][col] !== 0) {
        ctx.fillText(grid[row][col], col * cellSize + 15, row * cellSize + 35);
      }
    }
  }
}

// Function to update the game
function updateGame() {
  drawGrid();
  drawNumbers();
}

// Function to handle cell selection
canvas.addEventListener('click', function(event) {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  const row = Math.floor(y / cellSize);
  const col = Math.floor(x / cellSize);

  selectedCell = { row: row, col: col };
  updateGame();
});

// Function to handle keypress events for entering numbers
document.addEventListener('keydown', function(event) {
  if (selectedCell) {
    const key = event.key;
    if (key >= '1' && key <= '9') {
      grid[selectedCell.row][selectedCell.col] = parseInt(key);
    } else if (key === '0') {
      grid[selectedCell.row][selectedCell.col] = 0;  // Clear the cell
    }
    updateGame();
  }
});

// Function to clear the board when the "Clear" button is clicked
document.getElementById('clearButton').addEventListener('click', function() {
  grid = Array(9).fill().map(() => Array(9).fill(0));  // Reset the grid
  selectedCell = null;
  updateGame();
});

// Initial drawing of the grid and numbers
updateGame();
