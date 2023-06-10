from canvas import Canvas



matrix = [
    [1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
]

myCanvas = Canvas(matrix)
myCanvas.activeString = myCanvas.colors[0]
myCanvas.colorSquare(myCanvas.squares[0])
myCanvas.cutString()
myCanvas.colorSquare(myCanvas.squares[0])
myCanvas.colorSquare(myCanvas.squares[4])

print("DONE")