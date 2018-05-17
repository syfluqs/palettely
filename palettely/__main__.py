import numpy as np
from PIL import Image
import colorsys
from collections import deque
from termcolor import termcolor
from color_wheel import color_wheel
from color_wheel import color
import os

'''
http://www.aishack.in/tutorials/dominant-color/
'''

class palette_generator:
    classes = None
    im = None
    im_ = None
    tree_root = None

    def __init__(self,output_colors=20,subsampling_size=24):
        self.no_of_colors = output_colors
        self.subsampling_size = subsampling_size

    class tree_node:
        def __init__(self,classid):
            self.classid = classid
            self.right = None
            self.left = None
            self.cov = None
            self.mean = None

    @staticmethod
    def straighten(img):
        return np.ma.resize(img,(img.shape[0]*img.shape[1],3)).T

    @staticmethod
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

    @staticmethod
    def partition_node(node, nextid, img_shape):
        m = node.mean
        c = node.cov
        leftid = nextid
        rightid = nextid+1
        eigvals, eigvecs = np.linalg.eig(np.array(c))
        eigvecs = eigvecs[0]
        threshold = np.dot(eigvecs,m.T)

        node.left = palette_generator.tree_node(leftid)
        node.right = palette_generator.tree_node(rightid)

        for a in range(img_shape[0]):
            for b in range(img_shape[1]):
                if (palette_generator.classes[a,b]!=node.classid)[0]:
                    continue
                val = np.dot(eigvecs,palette_generator.im_[a,b].T)
                if (val<=threshold):
                    palette_generator.classes[a,b] = [leftid]*3
                else:
                    palette_generator.classes[a,b] = [rightid]*3

        return

    @staticmethod
    def get_mean_cov(node):
        masked_im = np.ma.masked_where((palette_generator.classes!=node.classid),palette_generator.im_)
        node.mean = np.mean(palette_generator.straighten(masked_im),1)
        node.cov = np.ma.cov(palette_generator.straighten(masked_im))

    @staticmethod
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

    @staticmethod
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
            
    @staticmethod
    def show_palette(leaf_nodes):
        im = im.resize((1024,720))
        palette = np.zeros((im.size[1],100,3),dtype=np.uint8)
        p_spac = im.size[1]//len(leaf_nodes)
        for i in range(len(leaf_nodes)-1):
            palette[p_spac*i:p_spac*(i+1),:,:] = np.array(leaf_nodes[i][1],dtype=np.uint8)
            print(color.rgb_box(np.array(leaf_nodes[i][1],dtype=np.uint8),n=4),end="")
        palette[p_spac*(len(leaf_nodes)-1):palette.shape[0]-1,:,:] = np.array(leaf_nodes[len(leaf_nodes)-1][1],dtype=np.uint8)
        print(color.rgb_box(np.array(leaf_nodes[len(leaf_nodes)-1][1],dtype=np.uint8),n=4))
        Image.fromarray((np.append(np.array(im),palette,axis=1))).show()
        
    @staticmethod
    def get_palette(leaf_nodes,sortby='area',option=None):
        palette = []
        for i in leaf_nodes:
            palette.append(tuple([int(x) for x in i[1]]))
        if (sortby=='saturation'):
            palette.sort(key=lambda tup:color.metric.normalized_saturation(*tup))
        elif (sortby=='value'):
            palette.sort(key=lambda tup:color.metric.normalized_value(*tup), reverse=True)
        elif (sortby=='saturation+value'):
            palette.sort(key=lambda tup:1-color.metric.normalized_saturation(*tup)+color.metric.normalized_value(*tup), reverse=True)
        elif (sortby=='standard_deviation' or sortby=='distance_from_gray'):
            palette.sort(key=lambda tup:1-color.metric.standard_deviation(*tup))
        elif (sortby=='nearest_to'):
            if type(option)!=tuple and len(option)!=3:
                raise Exception("Incorrect syntax for option argument")
            palette.sort(key=lambda tup:1-color.metric.color_distance(*tup,*option), reverse=True)
        return palette

    def generate(self, img_path, sortby="area", option=None):
        if (not os.path.isfile(img_path)):
            raise Exception("Image file not found")
            return
        palette_generator.im = Image.open(img_path).convert('RGB')
        im_r = palette_generator.im.resize((self.subsampling_size,self.subsampling_size))
        palette_generator.im_ = np.array(im_r, dtype=np.uint8)

        palette_generator.tree_root = palette_generator.tree_node(1)

        palette_generator.classes = np.ones(palette_generator.im_.shape,dtype=np.uint8)
        palette_generator.get_mean_cov(palette_generator.tree_root)
        for i in range(self.no_of_colors-1):
            # get max eigenvalue node
            m=palette_generator.get_max_eigenval_node(palette_generator.tree_root)
            # partition class
            palette_generator.partition_node(m,palette_generator.get_next_id(palette_generator.tree_root),palette_generator.im_.shape)
            # get mean cov of left and right
            palette_generator.get_mean_cov(m.left)
            palette_generator.get_mean_cov(m.right)

        tmp = palette_generator.get_palette(palette_generator.get_leaf_nodes(palette_generator.tree_root),sortby,option)

        palette_generator.classes = None
        palette_generator.im = None
        palette_generator.im_ = None
        palette_generator.tree_root = None

        return tmp

    def generate_from_dir(self, dir_path=".", sortby="area", option=None):
        if not os.path.isdir(dir_path):
            raise Exception("Directory not found")
            return
        ret = []
        for f in os.listdir(dir_path):
            f_ = f.lower()
            if (f_.endswith(".jpg") or f_.endswith(".jpeg") or f_.endswith(".png")):
                ret.append((self.generate(dir_path+"/"+f,sortby,option),f))
        return ret

if __name__ == '__main__':
    p = palette_generator()
    for j in p.generate_from_dir(sortby="standard_deviation"):
        line1 = []
        line2 = []
        line3 = []
        for i in j[0]:
            line1.append(termcolor.rgb_box(i,4))
            tmp = color_wheel.triadic(*i)
            line2.append(termcolor.rgb_box(tmp[0],4))
            line3.append(termcolor.rgb_box(tmp[1],4))

        print(j[1])
        print("".join(line1))
        # print("".join(line2))
        # print("".join(line3))