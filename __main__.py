import numpy as np
from PIL import Image
from collections import deque

'''
http://www.aishack.in/tutorials/dominant-color/
'''

classes = None

class tree_node:
    def __init__(self,classid):
        self.classid = classid
        self.right = None
        self.left = None
        self.cov = None
        self.mean = None

def straighten(img):
    return np.ma.resize(img,(img.shape[0]*img.shape[1],3)).T

def get_max_eigenval_node(tree_node):
    max_eigen = -1
    ret = None
    # if only one node in tree
    if tree_node.left==None and tree_node.right==None:
        return tree_node
    q = deque()
    q.append(tree_node)
    while (q):
        a = q.popleft()
        if (a.right!=None and a.left!=None):
            q.append(a.left)
            q.append(a.right)
            continue
        eigv = np.linalg.eigvals(a.cov)
        if (eigv[0]>max_eigen):
            max_eigen = eigv[0]
            ret = a
    return ret

def partition_node(node, nextid, img_shape):
    global last_id, classes
    m = node.mean
    c = node.cov
    leftid = nextid
    rightid = nextid+1
    eigvals, eigvecs = np.linalg.eig(np.array(c))
    eigvecs = eigvecs[0]
    threshold = np.dot(eigvecs,m.T)

    node.left = tree_node(leftid)
    node.right = tree_node(rightid)
    last_id = rightid+1

    for a in range(img_shape[0]):
        for b in range(img_shape[1]):
            if (classes[a,b]!=node.classid)[0]:
                continue
            val = np.dot(eigvecs,im_[a,b].T)
            if (val<=threshold):
                classes[a,b] = [leftid]*3
            else:
                classes[a,b] = [rightid]*3

    return

def get_mean_cov(node):
    global classes
    masked_im = np.ma.masked_where((classes!=node.classid),im_)
    node.mean = np.mean(straighten(masked_im),1)
    node.cov = np.ma.cov(straighten(masked_im))

def get_next_id(root_node):
    q = deque()
    max_id = 1
    if root_node.left==None and root_node.right==None:
        return max_id+1
    q.append(root_node)
    while (q):
        a = q.popleft()
        if a.classid>max_id:
            max_id=a.classid
        if (a.left!=None and a.right!=None):
            q.append(a.left)
            q.append(a.right)
    return max_id+1


def generate(node, colors):
    # Image.fromarray(im_).show()
    get_mean_cov(node)
    for i in range(colors-1):
        # get max eigenvalue node
        m=get_max_eigenval_node(node)
        # partition class
        partition_node(m,get_next_id(node),im_.shape)
        # get mean cov of left and right
        get_mean_cov(m.left)
        get_mean_cov(m.right)

def get_leaf_nodes(root_node):
    if root_node.left==None and root_node.right==None:
        return [1]
    ret = []
    q = deque()
    q.append(root_node)

    while (q):
        a = q.popleft()
        if (a.left==None and a.right==None):
            ret.append((a.classid,np.array(a.mean)))
        else:
            q.append(a.left)
            q.append(a.right)
    return ret
        
def generate_palette(leaf_nodes):
    global im
    im = im.resize((1024,720))
    palette = np.zeros((im.size[1],100,3),dtype=np.uint8)
    p_spac = im.size[1]//len(leaf_nodes)
    for i in range(len(leaf_nodes)-1):
        palette[p_spac*i:p_spac*(i+1),:,:] = np.array(leaf_nodes[i][1],dtype=np.uint8)
    palette[p_spac*(len(leaf_nodes)-1):palette.shape[0]-1,:,:] = np.array(leaf_nodes[len(leaf_nodes)-1][1],dtype=np.uint8)
    Image.fromarray((np.append(np.array(im),palette,axis=1))).show()
    


im = Image.open("/home/roy/projects/palettely/pexels-photo-248797.jpeg").convert('RGB')
no_of_colors = 20
im_r = im.resize((24,24))
im_ = np.array(im_r, dtype=np.uint8)

tree_root = tree_node(1)

classes = np.ones(im_.shape,dtype=np.uint8)
generate(tree_root,no_of_colors)

# for i in leaf:
#     Image.fromarray(np.ma.masked_where((classes!=i[0]),im_).filled(0)).show()
generate_palette(get_leaf_nodes(tree_root))