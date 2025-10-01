from PIL import Image
import numpy as np

img = Image.open("MazePhotoTerminal_3.png").convert("L")
img = np.array(img)
binary_img = (img > 127).astype(np.uint8)

def printImage(img):
    for row in range(len(binary_img[0])):
        for col in range(len(binary_img[1])):
            if binary_img[row,col] == 0:
                print(end="⬛")
            if binary_img[row,col] == 1:
                print(end="⬜")
            if binary_img[row,col] == 2:
                print(end="🟩")
        print()

            
def directionsCount(binary_img,x,y,px,py):
    directions = []
    for dx,dy in OFFSET:
        if binary_img.shape[0] > (x+dx) > 0 and binary_img.shape[0] > (y+dy) > 0:
            if binary_img[x+dx,y+dy] != 0 and (px,py) != (x+dx,y+dy):
                directions.append((dx,dy))
    return directions

OFFSET  = [[0,1],[0,-1],[1,0],[-1,0]]      
node_tree = {}
node_id = 1
total_path = []



def run2(x,y,px,py,path_pixel = None):
    global node_id,total_path
    directions = directionsCount(binary_img,x,y,px,py) # 0-3 directions
    if path_pixel is None:
        path_pixel = []
    path_pixel.append((x,y))

    if len(directions) == 1:
        while len(directions) == 1:
            dx, dy = directions[0]
            x, y, px, py = x+dx, y+dy, x, y
            path_pixel.append((x,y))
            directions = directionsCount(binary_img, x, y, px, py)
        run2(x, y, px, py,path_pixel[:])


    elif len(directions) > 1:
        node_tree[node_id] = (x,y,px,py,directions)
        save_node_id = node_id
        node_id += 1

        while node_tree[save_node_id][4]:
            dir = node_tree[save_node_id][4].pop(0)
            dx,dy = dir
            node_x,node_y = x+dx,y+dy
            run2(node_x,node_y,x,y,path_pixel[:])

    else:
        if (x,y) == (binary_img.shape[0]-2,binary_img.shape[0]-1):
            print("maze done")
            total_path.append(path_pixel[:])
        return
    
def imageShow(img):
    for x,y in total_path[0]:
        img[x,y] = 2
    return img

run2(1,0,0,0)
img= imageShow(binary_img)
printImage(img)

