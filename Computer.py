import Constants as c
from Pieces import listPiecestoArr
import Chess as ch

def getPlayInfo(listpieces, from_x, from_y, to_x, to_y, mgInit):
    pieces = movedeep(listpieces ,1 ,c.player2Color, from_x, from_y, to_x, to_y, mgInit)
    return [pieces[0].x, pieces[0].y, pieces[1], pieces[2]]

def movedeep(listpieces, deepstep, player, x1, y1, x2, y2, mgInit):
    # All time
    s = ch.step(8 - x1, y1, 8 - x2, y2)
    print(s)
    mgInit.move_to(s)
    mgInit.alpha_beta(c.max_depth, c.min_val, c.max_val)
    t = mgInit.best_move
    mgInit.move_to(t)
    print(mgInit.cnt)
    print("Annoying!")
    print(t)

    arr = listPiecestoArr(listpieces)
    listMoveEnabel = []
    for i in range(0, 9):
        for j in range(0, 10):
            for item in listpieces:
                if item.x == 8 - t.from_x and item.y == t.from_y:
                    listMoveEnabel.append([item, 8 - t.to_x, t.to_y])
    piecesbest = listMoveEnabel[0]
    return piecesbest