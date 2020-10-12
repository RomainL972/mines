$(document).ready(function() {
    var NUMBER_OF_ROWS = 9
    var NUMBER_OF_COLS = 9
    var NUMBER_OF_MINES = 10

    function isValidPos(x, y) {
        return !(x < 0 || x > NUMBER_OF_COLS-1 || y < 0 || y > NUMBER_OF_ROWS-1)
    }

    function initBoard() {
        board = []
        for (var i = 0; i < NUMBER_OF_COLS; i++) {
            board[i] = []
            for (var j = 0; j < NUMBER_OF_ROWS; j++) {
                board[i][j] = "?"
            }
        }
        return board
    }

    function initMines(board, x, y) {
        safe = []
        mines = []
        for (var i = x-1; i <= x+1; i++) {
            for (var j = y-1; j <= y+1; j++) {
                if (isValidPos(i, j)) {
                    safe.push([i, j])
                }
            }
        }

        for (var i = 0; i < NUMBER_OF_MINES; i++) {
            do {
                x = Math.floor(Math.random()*NUMBER_OF_COLS-1)
                y = Math.floor(Math.random()*NUMBER_OF_ROWS-1)
            } while (mines.includes([x, y]) || safe.includes([x, y]));
            mines.push([x, y])
        }
        return mines
    }

    function click(e) {
        e.preventDefault()
        x = Math.floor(e.offsetX / 500 * NUMBER_OF_COLS)
        y = Math.floor(e.offsetY / 500 * NUMBER_OF_ROWS)
        button = e.button
        if (button == 0) {
            if (!mines.length) {
                mines = initMines(board, x, y)
            }
            console.log(mines)
        }
    }

    board = initBoard()
    mines = []

    canvas = $("#canvas")
    canvas.click(click)
    canvas.contextmenu(click)
    context = canvas[0].getContext("2d")

    context.fillStyle = "blue"
    context.fillRect(0,0,500,500)

    context.fillStyle = "black"

    sizeCol = 500/NUMBER_OF_COLS
    sizeRow = 500/NUMBER_OF_ROWS

    for (i = 1; i <= NUMBER_OF_COLS; i++) {
      context.fillRect(sizeCol*i,0,1,500)
    }
    for (i = 1; i <= NUMBER_OF_ROWS; i++) {
      context.fillRect(0,sizeRow*i,500,1)
    }
})
