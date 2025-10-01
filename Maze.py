from PIL import Image
import numpy as np

def image_info(img):
    print("Format:", img.format)        
    print("Mode:", img.mode)            
    print("Size:", img.size)            
    print("Width:", img.width)
    print("Height:", img.height)

img = Image.open("MazePhoto.jpg")

# === Resize picture ===
size = 150
img_resized = img.resize((size, size))
image_info(img_resized)
#=======================

# === Transform to np.array for vectorize ===
# img_resized_np.shape = (size,size,3)
img_resized_np = np.array(img_resized)
#============================================

#=== Reshape to (size*size,RGB(3)) ===
# reshape.shape = (size*size,3)
reshape = img_resized_np.reshape(img_resized_np.shape[0]*img_resized_np.shape[1],3)
#=================================

# === change RGB channel to One channel (0/255) ===
# reshape_no_RGB.shape = (size*size,1)
reshape_no_RGB = reshape[:,0].reshape(-1,1)
#======================================================
ADJACENT_PIXLE_SCALLAR_LW_5 = [1,size,-size,size+1,-(size+1)]
ADJACENT_PIXLE_SCALLAR_RW_5 = [-1,size,-size,-(size+1),size -1]
ADJACENT_PIXLE_SCALLAR_UW_5 = [1,-1,150,151,149]
ADJACENT_PIXLE_SCALLAR_DW_5 = [1,-1,-size,-(size+1),-(size-1)]
ADJACENT_PIXLE_SCALLAR = [1,-1,size,-size,size+1,-(size+1),size -1,-(size -1)]
def pixleAdjacent(reshape_no_RGB):
    
    reshape_no_RGB_adjacent = [[0] for _ in range(size*size)]    
    
    for pixel in range(reshape_no_RGB.shape[0]):
        ADJACENT_PIXLE_GROUP = []
        
        if pixel % size == 0:
            offset =  ADJACENT_PIXLE_SCALLAR_RW_5
        elif pixel % size == size - 1:
            offset =  ADJACENT_PIXLE_SCALLAR_LW_5
        elif pixel <= size-1:
            offset =  ADJACENT_PIXLE_SCALLAR_UW_5
        elif pixel >= (size**2) - size:
            offset =  ADJACENT_PIXLE_SCALLAR_DW_5
        else: 
            offset =  ADJACENT_PIXLE_SCALLAR

        for i in offset:
            if 0 <= pixel + i < size**2:
                ADJACENT_PIXLE_GROUP.append(int(reshape_no_RGB[pixel+i,0]))
        average = int((sum(ADJACENT_PIXLE_GROUP))/len(ADJACENT_PIXLE_GROUP)+1)
        reshape_no_RGB_adjacent[pixel][0] = average
    
    return np.array(reshape_no_RGB_adjacent)
    

reshape_no_RGB_adjacent = pixleAdjacent(reshape_no_RGB)

mask = reshape_no_RGB_adjacent[:,0] > 245
reshape_no_RGB_adjacent[mask,0] = 1
reshape_no_RGB_adjacent[~mask,0] = 0


# === Build back the image ===
#binary_img.shape = (size,size)
binary_img = reshape_no_RGB_adjacent.reshape(img_resized_np.shape[0],img_resized_np.shape[1])
#=============================
#=== Remove outer area ===
pixle_to_change = [] #(row/col_num,row/col)
for i in range(binary_img.shape[0]):
    if np.all(binary_img[:,i]) !=0:
        pixle_to_change.append((i,1))
        
    if np.all(binary_img[i,:]) !=0:
        pixle_to_change.append((i,0))

for idx,kind in pixle_to_change:
    if kind == 1:
        binary_img[:,idx] = 0
    elif kind == 0:
        binary_img[idx,:] = 0
#=========================    
#=== Maze entrance/exit finder ===
for i in range(binary_img.shape[0]):
    if np.sum(binary_img[:,i]) != 0:
        for k in range(binary_img.shape[0]):
            if np.sum(binary_img[k,:]) != 0:        
                start_axis = (k,i)
                break
        break
#=================================
        
def Center_xy(binary_img,start_axis):
    x,y = start_axis
    dxup = x
    dxun = x
    dyup = y
    dyun = y

    while binary_img[dxup,y] and dxup < binary_img.shape[0] != 0:
        dxup  += 1
    
    while binary_img[dxun,y] and dxun < binary_img.shape[1] != 0:
        dxun -= 1

    x = int((dxun+dxup)/2)


    dyup = y
    dyun = y
    
    while binary_img[x,dyup] and dyup < binary_img.shape[0] != 0:
        dyup  += 1
    
    while binary_img[x,dyun] and dyun < binary_img.shape[1] != 0:
        dyun -= 1

    y = int((dyun+dyup)/2)
    
    return x,y

def directionsCount(binary_img,x,y,px,py):
    directions = []
    for dx,dy in OFFSET:
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
        if (x,y) == (141,147):
            print("===========")
            print("Maze solved")
            print("===========")

            total_path.append(path_pixel[:])
        return
def imageShow(binary_photo,img_resized_np):
    # binary_photo_shape(size**2(1/0),1)
    mask = binary_photo[:,0] == 1
    binary_photo = binary_photo * 255
    image = binary_photo.reshape(img_resized_np.shape[0],img_resized_np.shape[1])
        
    image_rgb = np.stack([image, image, image], axis=-1)
    for x,y in total_path[0]:
        image_rgb[x,y] = [0,255,0]


    Image.fromarray(image_rgb.astype("uint8")).show()

run2(8,2,0,0)

imageShow(binary_img,img_resized_np)

    
    

