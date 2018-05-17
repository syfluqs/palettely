import colorsys

class color_wheel:

    @staticmethod
    def split_complementary(R,G,B,n=2,spacing=72):
        ret = []
        spacing %= 360
        spacing /= 360
        hue, sat, val = colorsys.rgb_to_hsv(R/255.0,G/255.0,B/255.0)
        comp_hue = 0.5+hue
        if comp_hue>1.0:
            comp_hue -= 1.0
        if (n%2):
            # n is odd
            start = comp_hue-((n-1)/2)*spacing
            if (start<0.0):
                start += 1.0
        else:
            # n is even
            start = comp_hue-(spacing/2)-(n/2-1)*spacing
            if (start<0.0):
                start += 1.0
        for i in range(n):
            ret_r, ret_g, ret_b = colorsys.hsv_to_rgb(start,sat,val)
            start += spacing
            if (start>1.0):
                start -= 1.0
            elif (start<0.0):
                start += 1.0
            ret.append((int(ret_r*255), int(ret_g*255), int(ret_b*255)))
        return ret

    @staticmethod
    def complementary(R,G,B):
        return (color_wheel.split_complementary(R,G,B,n=1)[0])

    @staticmethod
    def triadic(R,G,B):
        return (color_wheel.split_complementary(R,G,B,n=2,spacing=120))

    @staticmethod
    def tetradic(R,G,B):
        return (color_wheel.split_complementary(R,G,B,n=3,spacing=90))

    @staticmethod
    def analogous(R,G,B,spacing=72):
        return (color_wheel.split_complementary(R,G,B,n=2,spacing=360-spacing))


class color:

    @staticmethod
    def to_hex(R,G,B):
        def clamp(x): 
            return max(0, min(x, 255))
        return "#{0:02x}{1:02x}{2:02x}".format(clamp(R), clamp(G), clamp(B))

    @staticmethod
    def to_hex_alpha(R,G,B,A):
        def convert(A):
            return int(A*255)
        return color.to_hex(R,G,B)+"{0:02x}".format(convert(A))

    class metric:
        @staticmethod
        def normalized_saturation(R,G,B):
            return colorsys.rgb_to_hsv(R/255.0, G/255.0, B/255.0)[0]

        @staticmethod
        def normalized_value(R,G,B):
            return colorsys.rgb_to_hsv(R/255.0, G/255.0, B/255.0)[2]

        @staticmethod
        def standard_deviation(R,G,B):
            mean = (R+G+B)/3
            return ((R-mean)**2+(G-mean)**2+(B-mean)**2)

        @staticmethod
        def color_distance(R,G,B,R_t,G_t,B_t):
            return ((R-R_t)**2+(G-G_t)**2+(B-B_t)**2)