const canvas = document.getElementById('sudokuCanvas');
const ctx = canvas.getContext('2d');
const cellSize = 50;
let grid = Array(9).fill().map(() => Array(9).fill(0)); // 9x9 grid initialized to 0

// Function to draw the grid
function drawGrid() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i <= 9; i++) {
    let thickness = i % 3 === 0 ? 3 : 1;
    ctx.beginPath();
    ctx.moveTo(i * cellSize, 0);
    ctx.lineTo(i * cellSize, canvas.height);
    ctx.moveTo(0, i * cellSize);
    ctx.lineTo(canvas.width, i * cellSize);
    ctx.lineWidth = thickness;
    ctx.stroke();
  }
}

drawGrid();

// Add Sudoku logic here
// Hook up Solve and Clear button functionality
document.getElementById('solveButton').addEventListener('click', function() {
  // Implement the solving logic
});

document.getElementById('clearButton').addEventListener('click', function() {
  grid = Array(9).fill().map(() => Array(9).fill(0));
  drawGrid();
});
