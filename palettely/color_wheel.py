'''
           _                       _               _ 
          | |                     | |             | |
  ___ ___ | | ___  _ __  __      _| |__   ___  ___| |
 / __/ _ \| |/ _ \| '__| \ \ /\ / / '_ \ / _ \/ _ \ |
| (_| (_) | | (_) | |     \ V  V /| | | |  __/  __/ |
 \___\___/|_|\___/|_|      \_/\_/ |_| |_|\___|\___|_|
                                                     

'''

import colorsys

class color_wheel:
    ''' Color Wheel class
        Contains functions for all various harmony schemes
    '''

    @staticmethod
    def complementary(R,G,B):
        ''' Complmentary Harmony, also called Direct Harmony
        
        Returns the color directly opposite to the input color
        
        Arguments:
            R {int} -- 0-255, Red value in RGB colorspace
            G {int} -- 0-255, Green value in RGB colorspace
            B {int} -- 0-255, Blue value in RGB colorspace
        '''
        return (color_wheel.split_complementary(R,G,B,n=1)[0])

    @staticmethod
    def split_complementary(R,G,B,n=2,spacing=72):
        ''' Split Complementary Harmony
        
        Returns n colors directly opposite to the input color, separated by some
        angle on the color wheel
        
        Arguments:
            R {int} -- 0-255, Red value in RGB colorspace
            G {int} -- 0-255, Green value in RGB colorspace
            B {int} -- 0-255, Blue value in RGB colorspace
        
        Keyword Arguments:
            n {number} -- Number of colors to return (default: {2})
            spacing {number} -- Spacing, in degrees, between any two consecutive
                                split complementary colors on color wheel 
                                (default: {72})
        
        Returns:
            list -- list of length n, contains tuples corresponding to the split
                    complementary colors
        '''
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
    def triadic(R,G,B):
        ''' Triadic Harmony
        
        Returns two colors, such that these colors and the input color form an
        equilateral triangle on the color wheel
        
        Arguments:
            R {int} -- 0-255, Red value in RGB colorspace
            G {int} -- 0-255, Green value in RGB colorspace
            B {int} -- 0-255, Blue value in RGB colorspace
        '''
        return (color_wheel.split_complementary(R,G,B,n=2,spacing=120))

    @staticmethod
    def tetradic(R,G,B):
        ''' Tetradic Harmony, also called Square Harmony
        
        Return three colors, such that these colors and the input color form a
        square on the color wheel
        
        Arguments:
            R {int} -- 0-255, Red value in RGB colorspace
            G {int} -- 0-255, Green value in RGB colorspace
            B {int} -- 0-255, Blue value in RGB colorspace
        '''
        return (color_wheel.split_complementary(R,G,B,n=3,spacing=90))

    @staticmethod
    def analogous(R,G,B,spacing=72):
        ''' Analogous Harmony
        
        Returns two colors which are adjoining to the input color, separated by
        an angle.
        
        Arguments:
            R {int} -- 0-255, Red value in RGB colorspace
            G {int} -- 0-255, Green value in RGB colorspace
            B {int} -- 0-255, Blue value in RGB colorspace
        
        Keyword Arguments:
            spacing {number} -- Angle of separation between returned colors
                                (default: {72})
        '''
        return (color_wheel.split_complementary(R,G,B,n=2,spacing=360-spacing))


class color:

    @staticmethod
    def to_hex(R,G,B):
        ''' Make HTML hex code from RGB color
        
        Arguments:
            R {int} -- 0-255, Red value in RGB colorspace
            G {int} -- 0-255, Green value in RGB colorspace
            B {int} -- 0-255, Blue value in RGB colorspace
        
        Returns:
            str -- hex code in the format #rrggbb
        '''
        def clamp(x): 
            return max(0, min(x, 255))
        return "#{0:02x}{1:02x}{2:02x}".format(clamp(R), clamp(G), clamp(B))

    @staticmethod
    def to_hex_alpha(R,G,B,A):
        ''' Make HTML hex code (with alpha value) with RGBA color
        
        Arguments:
            R {int} -- 0-255, Red value in RGB colorspace
            G {int} -- 0-255, Green value in RGB colorspace
            B {int} -- 0-255, Blue value in RGB colorspace
            A {double} -- 0.0-1.0, Alpha value
        
        Returns:
            str -- hex code in the format #rrggbbaa
        '''
        def convert(A):
            return int(A*255)
        return color.to_hex(R,G,B)+"{0:02x}".format(convert(A))

    class metric:
        ''' Metric class

            Contains several functions to assess colors
        '''
        @staticmethod
        def normalized_saturation(R,G,B):
            ''' Returns normalized saturation of the input color
            
            Arguments:
                R {int} -- 0-255, Red value in RGB colorspace
                G {int} -- 0-255, Green value in RGB colorspace
                B {int} -- 0-255, Blue value in RGB colorspace
            
            Returns:
                double -- 0.0-1.0, double value
            '''
            return colorsys.rgb_to_hsv(R/255.0, G/255.0, B/255.0)[0]

        @staticmethod
        def normalized_value(R,G,B):
            ''' Returns normalized value of the input color
            
            Arguments:
                R {int} -- 0-255, Red value in RGB colorspace
                G {int} -- 0-255, Green value in RGB colorspace
                B {int} -- 0-255, Blue value in RGB colorspace
            
            Returns:
                double -- 0.0-1.0, double value
            '''
            return colorsys.rgb_to_hsv(R/255.0, G/255.0, B/255.0)[2]

        @staticmethod
        def standard_deviation(R,G,B):
            ''' Returns standard deviation between Red, Green and Blue values 
                of the input color
            
            Arguments:
                R {int} -- 0-255, Red value in RGB colorspace
                G {int} -- 0-255, Green value in RGB colorspace
                B {int} -- 0-255, Blue value in RGB colorspace
            
            Returns:
                double -- standard deviation
            '''
            mean = (R+G+B)/3
            return ((R-mean)**2+(G-mean)**2+(B-mean)**2)

        @staticmethod
        def color_distance(R,G,B,R_t,G_t,B_t):
            ''' Returns distance of the input color (R,G,B) from target color
                (R_t, G_t, B_t)
            
            Arguments:
                R {int} -- 0-255, Red value in RGB colorspace
                G {int} -- 0-255, Green value in RGB colorspace
                B {int} -- 0-255, Blue value in RGB colorspace
                R_t {int} -- 0-255, Target Red value in RGB colorspace
                G_t {int} -- 0-255, Target Green value in RGB colorspace
                B_t {int} -- 0-255, Target Blue value in RGB colorspace

            
            Returns:
                double -- Distance metric
            '''
            return ((R-R_t)**2+(G-G_t)**2+(B-B_t)**2)