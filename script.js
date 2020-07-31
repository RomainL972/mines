function click(e) {
    e.preventDefault()
    x = e.offsetX
    y = e.offsetY
    button = e.button
    console.log("" + Math.floor(x / 500 * numberOfMines) + " " + Math.floor(y / 500 * numberOfMines))
    console.log(e.button)
}

numberOfMines = 9
canvas = $("#canvas")
canvas.click(click)
canvas.contextmenu(click)
context = canvas[0].getContext("2d")

context.fillStyle = "blue"
context.fillRect(0,0,500,500)

context.fillStyle = "black"
size = 500/numberOfMines
for (i = 1; i <= 9; i++) {
  context.fillRect(size*i,0,1,500)
  context.fillRect(0,size*i,500,1)
}
