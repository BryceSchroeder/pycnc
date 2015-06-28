# -*- coding: utf-8 -*-

import math
import os

GCODE_EXTENSION = '.ngc'

########################################################################
#                      GCODE GENERATION                                #
########################################################################

def oval(x_center,
         y_center,
         x_width,
         y_height,
         tool_diameter,
         feed_rate,
         z_feed_rate,
         from_z,
         to_z,
         step_z,
         safety_z,
         angle=0.0):#clockwise rotation angle
         
    """Generate Gcode to cut an oval"""

    point_center = Point(x_center,y_center)

    gcode = []
    gcode.append(g0_gcode(x=x_center,y=y_center,z=safety_z))

    for h in generate_heights(from_z,to_z,step_z):
        for d in generate_excentric(0.00, y_height/2.0, tool_diameter):
            point_N = (Point(0.0,d) + point_center).rotate(point_center, angle)
            point_NE = (Point((x_width-y_height)/2.0,d)+ point_center).rotate(point_center, angle)
            point_E_arc_center = (Point((x_width-y_height)/2.0,0.0)+ point_center).rotate(point_center, angle)
            point_SE = (Point((x_width-y_height)/2.0,-d)+ point_center).rotate(point_center, angle)
            point_SW = (Point(-(x_width-y_height)/2.0,-d)+ point_center).rotate(point_center, angle)
            point_W_arc_center = (Point(-(x_width-y_height)/2.0,0.0)+ point_center).rotate(point_center, angle)
            point_NW = (Point(-(x_width-y_height)/2.0,d)+ point_center).rotate(point_center, angle)
            
            gcode.append(g1_gcode(z=h,feedrate=z_feed_rate))
            gcode.append(g1_gcode(x=point_N.x,y=point_N.y,feedrate=feed_rate))
            gcode.append(g1_gcode(x=point_NE.x,y=point_NE.y,feedrate=feed_rate))
            gcode.append(g2_gcode(x_end_point=point_SE.x,
                                    y_end_point=point_SE.y,
                                    spiral_end_altitude = h, 
                                    x_center_offset = (point_E_arc_center - point_NE).x,
                                    y_center_offset = (point_E_arc_center - point_NE).y,
                                    feedrate=feed_rate))
            gcode.append(g1_gcode(x=point_SW.x,y=point_SW.y,feedrate=feed_rate))
            gcode.append(g2_gcode(x_end_point=point_NW.x,
                                    y_end_point=point_NW.y,
                                    spiral_end_altitude = h, 
                                    x_center_offset = (point_W_arc_center - point_SW).x,
                                    y_center_offset = (point_W_arc_center - point_SW).y,
                                    feedrate=feed_rate))
            gcode.append(g1_gcode(x=point_N.x,y=point_N.y,feedrate=feed_rate))

    
    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    return ''.join(gcode)


def path(path,feed_rate,z_feed_rate,from_z,to_z,step_z,safety_z):
    
    """Generate Gcode to follow a path"""
    
    gcode = []
    gcode.append(g0_gcode(x=0,y=0,z=safety_z))
    gcode.append(g0_gcode(x=path[0][0],
                          y=path[0][1]))
    for h in generate_heights(from_z,to_z,step_z):
        gcode.append(g1_gcode(z=h,feedrate=z_feed_rate))
        for point in path:
            gcode.append(g1_gcode(x=point[0],y=point[1],feedrate=feed_rate))
    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    return ''.join(gcode)


def rectangle(x_dimension, # positive
              y_dimension, # positive
              x_mini,
              y_mini,
              tool_diameter,
              feed_rate, # mm/min
              z_feed_rate,
              from_z,
              to_z,
              step_z,
              safety_z):
                  
    """Generate Gcode to cut a rectangle

    The milling head travels CCW around the rectangle
    
    """
    
    gcode = []
    gcode.append(g0_gcode(x=0,y=0,z=safety_z))
    gcode.append(g0_gcode(x=x_mini-tool_diameter/2,
                          y=y_mini-tool_diameter/2))

    for h in generate_heights(from_z,to_z,step_z): 
        gcode.append(g1_gcode(z=h,feedrate=z_feed_rate))
        gcode.append(g1_gcode(x=x_mini+x_dimension+tool_diameter/2,feedrate=feed_rate))
        gcode.append(g1_gcode(y=y_mini+y_dimension+tool_diameter/2,feedrate=feed_rate))
        gcode.append(g1_gcode(x=x_mini-tool_diameter/2,feedrate=feed_rate))
        gcode.append(g1_gcode(y=y_mini-tool_diameter/2,feedrate=feed_rate))

    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    
    return ''.join(gcode)


def rectangle_rounded_corners(x_center,
                              y_center,
                              x_dimension,
                              y_dimension,
                              corner_radius,
                              tool_diameter,
                              feed_rate, # mm/min
                              z_feed_rate,
                              from_z,
                              to_z,
                              step_z,
                              safety_z):
                                  
    """Generate Gcode to cut a rectangle with rounded corners

    The milling head travels CCW around the rectangle
    
    """
    
    gcode = []
    gcode.append(g0_gcode(x=0,y=0,z=safety_z))
    # go to start point (LOWER LEFT CORNER)
    gcode.append(g0_gcode(x=x_center-x_dimension/2+corner_radius,
                          y=y_center-y_dimension/2-tool_diameter/2))

    for h in generate_heights(from_z,to_z,step_z): 
        gcode.append(g1_gcode(z=h,feedrate=z_feed_rate))
        # LOWER EDGE
        gcode.append(g1_gcode(x=x_center+x_dimension/2-corner_radius,feedrate=feed_rate))
        # BOTTOM RIGHT CORNER
        gcode.append(g3_gcode(x_end_point=x_center+x_dimension/2+tool_diameter/2,
                              y_end_point=y_center-y_dimension/2+corner_radius,
                              x_center_offset=0.0,
                              y_center_offset=corner_radius+tool_diameter/2,
                              spiral_end_altitude=h,
                              feedrate=feed_rate))
        # RIGHT EDGE
        gcode.append(g1_gcode(y=y_center+y_dimension/2-corner_radius,feedrate=feed_rate))
        # UPPER RIGHT CORNER
        gcode.append(g3_gcode(x_end_point=x_center+x_dimension/2-corner_radius,
                              y_end_point=y_center+y_dimension/2+tool_diameter/2,
                              x_center_offset=-corner_radius-tool_diameter/2,
                              y_center_offset=0.0,
                              spiral_end_altitude=h,
                              feedrate=feed_rate))
        # TOP EDGE
        gcode.append(g1_gcode(x=x_center-x_dimension/2+corner_radius,feedrate=feed_rate))
        gcode.append(g3_gcode(x_end_point=x_center-x_dimension/2-tool_diameter/2,
                              y_end_point=y_center+y_dimension/2-corner_radius,
                              x_center_offset=0.0,
                              y_center_offset=-corner_radius-tool_diameter/2,
                              spiral_end_altitude=h,
                              feedrate=feed_rate))
        gcode.append(g1_gcode(y=y_center-y_dimension/2+corner_radius,feedrate=feed_rate))
        gcode.append(g3_gcode(x_end_point=x_center-x_dimension/2+corner_radius,
                              y_end_point=y_center-y_dimension/2-tool_diameter/2,
                              x_center_offset=corner_radius+tool_diameter/2,
                              y_center_offset=0.0,
                              spiral_end_altitude=h,
                              feedrate=feed_rate))

    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    
    return ''.join(gcode)


def thin_from_center(x_dimension,
                     y_dimension,
                     x_center,
                     y_center,
                     tool_diameter,
                     feed_rate,
                     z_feed_rate,
                     from_z,
                     to_z,
                     step_z,
                     safety_z):
                         
    """Generate Gcode to remove some material from a region around the center of the region

    It is intended to be used to make the stock thinner over a region
    before cutting a part from the thinned region
    
    """
    
    return thin(x_dimension,
                y_dimension,
                x_center - x_dimension/2.0,
                y_center - y_dimension/2.0,
                tool_diameter,
                feed_rate,
                z_feed_rate,
                from_z,
                to_z,
                step_z,
                safety_z)

def thin(x_dimension,
         y_dimension,
         x_mini,
         y_mini,
         tool_diameter,
         feed_rate,
         z_feed_rate,
         from_z,
         to_z,
         step_z,
         safety_z):
             
    """Generate Gcode to remove some material from a region defined by the bottom left point 
    of a rectangle and its dimensions

    It is intended to be used to make the stock thinner over a region
    before cutting a part from the thinned region
    
    """
    
    x_center = x_mini+x_dimension/2;
    y_center = y_mini+y_dimension/2
    gcode = []
    gcode.append(g0_gcode(x=0,y=0,z=safety_z))
    gcode.append(g0_gcode(x=x_center,
                          y=y_center))
    

    for h in generate_heights(from_z,to_z,step_z):
        gcode.append(g1_gcode(x=x_center,y=y_center,feedrate=feed_rate))
        gcode.append(g1_gcode(z=h,feedrate=z_feed_rate))
        
        nb_turns = 0.00
        # correction bug 25 SEP 2012 - parcours du perimetre exterieur sans prendre de matiere
        # division par 2 de y_dimension dans l expression de la boucle while
        #while nb_turns/2*tool_diameter < x_dimension/2 or nb_turns/2*tool_diameter < y_dimension:
        while nb_turns/2*tool_diameter < x_dimension/2 or nb_turns/2*tool_diameter < y_dimension/2:
            gcode.append(g1_gcode(y=min(y_center+(nb_turns/2+0.5)*tool_diameter,y_mini+y_dimension-tool_diameter/2),feedrate=feed_rate))
            gcode.append(g1_gcode(x=min(x_center+(nb_turns/2+0.5)*tool_diameter,x_mini+x_dimension-tool_diameter/2),feedrate=feed_rate))
            gcode.append(g1_gcode(y=max(y_center-(nb_turns/2+0.5)*tool_diameter,y_mini+tool_diameter/2),feedrate=feed_rate))
            gcode.append(g1_gcode(x=max(x_center-(nb_turns/2+0.5)*tool_diameter,x_mini+tool_diameter/2),feedrate=feed_rate))
            gcode.append(g1_gcode(y=min(y_center+(nb_turns/2+0.5)*tool_diameter,y_mini+y_dimension-tool_diameter/2),feedrate=feed_rate))
            gcode.append(g1_gcode(x=x_center,feedrate=feed_rate))
            
            nb_turns = nb_turns +1.00

    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    
    return ''.join(gcode)


def hole(x_center,
         y_center,
         hole_diameter,
         tool_diameter,
         feed_rate,
         z_feed_rate,
         from_z,
         to_z,
         step_z,
         safety_z):
             
    """Generate Gcode to cut a hole

    If the hole diameter is bigger than 2 x tool_diameter the material in the center is not removed
    
    """
    
    if hole_diameter < tool_diameter:
        raise WrongParameterError('Cannot make a hole smaller than the tool')
    gcode = []
    gcode.append(g0_gcode(z=safety_z))
    gcode.append(g0_gcode(x=x_center-hole_diameter/2+tool_diameter/2,y=y_center))

    for h in generate_heights(from_z,to_z,step_z):
        gcode.append(g2_gcode(x_center_offset=hole_diameter/2-tool_diameter/2,y_center_offset=0,spiral_end_altitude=h,feedrate=feed_rate))
        
    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    
    return ''.join(gcode)

# *************************************************************************
# Full Hole
#     This function generates the gcode to cut a hole and remove the middle material
# *************************************************************************
def full_hole(x_center,
              y_center,
              hole_diameter,
              tool_diameter,
              feed_rate,
              z_feed_rate,
              from_z,
              to_z,
              step_z,
              safety_z,
              center_diameter = 0.0000):
                  
    """Generate Gcode to cut a hole and remove the middle material

    If the hole diameter is bigger than 2 x tool_diameter the material in the center is removed
    
    """
    if hole_diameter < tool_diameter:
        raise WrongParameterError('Cannot make a hole smaller than the tool')
    gcode = []
    gcode.append(g0_gcode(z=safety_z))
    #gcode.append(g0_gcode(x=x_center-tool_diameter/2,y=y_center))
    gcode.append(g0_gcode(x=x_center-tool_diameter/2,y=y_center))

    for h in generate_heights(from_z,to_z,step_z):
        gcode.append(g1_gcode(z=h,feedrate=z_feed_rate))
        for e in generate_excentric(start=center_diameter/2.0,end=hole_diameter/2,tool_diameter=tool_diameter):
            gcode.append(g1_gcode(x=x_center-e,y=y_center,feedrate=feed_rate))
            gcode.append(g2_gcode(x_center_offset=e,y_center_offset=0,spiral_end_altitude=h,feedrate=feed_rate))
        
    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    
    return ''.join(gcode)


def square_pocket(x_center,
                  y_center,
                  x_dimension,
                  y_dimension,
                  tool_diameter,
                  feed_rate,
                  z_feed_rate,
                  from_z,
                  to_z,
                  step_z,
                  safety_z):
                      
    """Generate Gcode to dig a square and remove the middle material"""
    
    if x_dimension < tool_diameter or y_dimension < tool_diameter:
        raise WrongParameterError('Cannot make a square pocket smaller than the tool')

    gcode = []
    gcode.append(g0_gcode(x=0,y=0,z=safety_z))
    gcode.append(g0_gcode(x=x_center,
                          y=y_center))
    
    x_absolute_maximum = x_center + x_dimension/2
    x_absolute_minimum = x_center - x_dimension/2
    
    x_maximum = x_absolute_maximum-tool_diameter/2
    x_minimum = x_absolute_minimum+tool_diameter/2
    
    y_maximum = y_center+y_dimension/2-tool_diameter/2
    y_minimum = y_center-y_dimension/2+tool_diameter/2
    
    path = []

    point1=[x_center,y_maximum]
    point2=[x_absolute_maximum,y_maximum]
    point3=[x_maximum,y_maximum]
    point4=[x_maximum,y_minimum]
    point5=[x_absolute_maximum,y_minimum]
    point6=[x_absolute_minimum,y_minimum]
    point7=[x_minimum,y_minimum]
    point8=[x_minimum,y_maximum]
    point9=[x_absolute_minimum,y_maximum]


    path.append(point1)
    path.append(point2)
    path.append(point3)
    path.append(point4)
    path.append(point5)
    path.append(point6)
    path.append(point7)
    path.append(point8)
    path.append(point9)
    path.append(point1)
    

    for h in generate_heights(from_z,to_z,step_z):
        gcode.append(g1_gcode(x=x_center,y=y_center,feedrate=feed_rate))
        gcode.append(g1_gcode(z=h,feedrate=z_feed_rate))
        
        nb_turns = 0.00
        
        while nb_turns/2*tool_diameter < x_dimension/2 or nb_turns/2*tool_diameter < y_dimension/2.0:
            y_maxi = min(y_center+(nb_turns/2+0.5)*tool_diameter,y_center+y_dimension/2-tool_diameter/2)
            x_maxi = min(x_center+(nb_turns/2+0.5)*tool_diameter,x_center+x_dimension/2-tool_diameter/2)
            y_mini = max(y_center-(nb_turns/2+0.5)*tool_diameter,y_center-y_dimension/2+tool_diameter/2)
            x_mini = max(x_center-(nb_turns/2+0.5)*tool_diameter,x_center-x_dimension/2+tool_diameter/2)
            
            
            gcode.append(g1_gcode(y=y_maxi,feedrate=feed_rate))
            gcode.append(g1_gcode(x=x_maxi,feedrate=feed_rate))
            gcode.append(g1_gcode(y=y_mini,feedrate=feed_rate))
            gcode.append(g1_gcode(x=x_mini,feedrate=feed_rate))
            gcode.append(g1_gcode(y=y_maxi,feedrate=feed_rate))
            gcode.append(g1_gcode(x=x_center,feedrate=feed_rate))
            
            nb_turns = nb_turns +1.00
            
        # Cut the corners
        for point in path:
            gcode.append(g1_gcode(x=point[0],y=point[1],feedrate=feed_rate))

    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    
    return ''.join(gcode)


def cylinder(x_center,
             y_center,
             cylinder_diameter,
             tool_diameter,
             feed_rate,
             z_feed_rate,
             from_z,
             to_z,
             step_z,
             safety_z):
                 
    """Generate Gcode to cut a cylinder"""
    
    gcode = []
    gcode.append(g0_gcode(z=safety_z))
    gcode.append(g0_gcode(x=x_center-(cylinder_diameter+tool_diameter)/2+tool_diameter/2,y=y_center))

    for h in generate_heights(from_z,to_z,step_z):
        gcode.append(g3_gcode(x_center_offset=(cylinder_diameter+tool_diameter)/2-tool_diameter/2,y_center_offset=0,spiral_end_altitude=h,feedrate=feed_rate))
        
    gcode.append(g1_gcode(z=safety_z,feedrate=feed_rate))
    
    return ''.join(gcode)



def two_concentric_holes(x_center,
         y_center,
         hole_diameter_1,
         hole_diameter_2,
         tool_diameter,
         feed_rate,
         z_feed_rate,
         from_z_1,
         to_z_1, # end of 1st hole, start of 2nd
         to_z_2,
         step_z,
         safety_z):
             
    """Generate Gcode to cut two concentric holes"""
    
    if hole_diameter_2 > hole_diameter_1:
        raise WrongParameterError('hole number 2 has to be smaller than hole number 1')
    gcode = []
    gcode.append(full_hole(x_center,
         y_center,
         hole_diameter_1,
         tool_diameter,
         feed_rate,
         z_feed_rate,
         from_z_1,
         to_z_1,
         step_z,
         safety_z))
    gcode.append(full_hole(x_center,
         y_center,
         hole_diameter_2,
         tool_diameter,
         feed_rate,
         z_feed_rate,
         to_z_1,
         to_z_2,
         step_z,
         safety_z))
    return ''.join(gcode)



def drill(x,y,depth,safety_height,feedrate):
    """Generate Gcode to drill at x,y"""
    gcode = []
    #gcode.append('G98\n')
    gcode.append(g0_gcode(z=safety_height))
    gcode.append(g0_gcode(x=x,y=y))
    gcode.append(g81_gcode(z=depth,r=safety_height,feedrate=feedrate))
    return ''.join(gcode)

def drill_g73(x,y,depth,depth_increment,safety_height,feedrate):
    """Generate Gcode to drill at x,y with chip breaking"""
    gcode = []
    #gcode.append('G98\n')
    gcode.append(g0_gcode(z=safety_height))
    gcode.append(g0_gcode(x=x,y=y))
    gcode.append(g73_gcode(z=depth,r=safety_height,q=depth_increment,feedrate=feedrate))
    return ''.join(gcode)

def drill_g83(x,y,depth,depth_increment,safety_height,feedrate):
    """Generate Gcode to peck drill at x,y"""
    gcode = []
    #gcode.append('G98\n')
    gcode.append(g0_gcode(z=safety_height))
    gcode.append(g0_gcode(x=x,y=y))
    gcode.append(g83_gcode(z=depth,r=safety_height,q=depth_increment,feedrate=feedrate))
    return ''.join(gcode)
    




def start_gcode():
    
    """Returns the codes that should be at the beginning of every NC file"""
    
    start_gcode = ['G21\n',  # millimeters G20:inches
                   'G17\n',  # XY plane selection
                   'G90\n', # absolute distance mode G91: incremental distance mode
                   'G54\n', # first coordinate system
                   'G40\n', # cancel cutter radius compensation
                   'G49\n', # cancel tool length offset
                   'G61\n', # exact path mode G61.1: exact stop mode G64: continuous mode with optional path tolerance
                   'G94\n'] # units per minute feed rate G93: inverse time feed rate G95: units per revolution
    return ''.join(start_gcode)


def end_gcode():
    
    """Returns the codes that should be at the end of every NC file"""
    
    end_gcode = ['M2\n'] # end program
    return ''.join(end_gcode)



########################################################################
#                      GCODE FORMATTING                                #
########################################################################

def gcode_format(prefix,x=None,y=None,z=None,i=None,j=None,r=None,q=None,feedrate=None):

    """Formats the Gcode line discarding undefined parameters"""

    gcode=[]
    gcode.append(prefix)
    gcode.append(' ')
    if x!=None: gcode.append('X%(x)s '%{'x':x})
    if y!=None: gcode.append('Y%(y)s '%{'y':y})
    if z!=None: gcode.append('Z%(z)s '%{'z':z})
    if i!=None: gcode.append('I%(i)s '%{'i':i})
    if j!=None: gcode.append('J%(j)s '%{'j':j})
    if r!=None: gcode.append('R%(r)s '%{'r':r})
    if q!=None: gcode.append('Q%(q)s '%{'q':q})
    if feedrate!=None: gcode.append('F%(f)s '%{'f':feedrate})
    gcode.append('\n')
    return ''.join(gcode)



def g0_gcode(x=None,y=None,z=None):
    """ Max speed move Gcode"""
    if x==None and y==None and z==None:
        raise GcodeParameterError('G0 parameter error')
    return gcode_format(prefix='G0',x=x,y=y,z=z)


def g1_gcode(x=None,y=None,z=None,feedrate=None):
    """ Feed speed move Gcode"""
    if x==None and y==None and z==None:
        raise GcodeParameterError('G1 parameter error')
    return gcode_format(prefix='G1',x=x,y=y,z=z,feedrate=feedrate)



def g2_gcode(x_end_point=None,
            y_end_point=None,
            spiral_end_altitude = None,
            x_center_offset=None,
            y_center_offset=None,
            feedrate=None):
    """ Clockwise arc"""
    if x_center_offset==None and y_center_offset==None:
        raise GcodeParameterError('G2 parameter error')
    return gcode_format(prefix='G2',x=x_end_point,y=y_end_point,z=spiral_end_altitude,i=x_center_offset,j=y_center_offset,feedrate=feedrate)


def g3_gcode(x_end_point=None,
            y_end_point=None,
            x_center_offset=None,
            y_center_offset=None,
            spiral_end_altitude=None,
            feedrate=None):
    """ Counterclockwise arc"""
    if x_center_offset==None and y_center_offset==None:
        raise GcodeParameterError('G3 parameter error')
    return gcode_format(prefix='G3',x=x_end_point,y=y_end_point,i=x_center_offset,j=y_center_offset,z=spiral_end_altitude,feedrate=feedrate)


def g73_gcode(x=None,
              y= None,
              z= None,
              r=None,
              q = None,
              feedrate=None):
    """ Chip break drill"""
    if z==None or r==None:
        raise GcodeParameterError('G73 parameter error')
    if r<z:
        raise GcodeParameterError('G73 parameter error - r smaller than z')
    return gcode_format(prefix='G73 G98',x=x,y=y,z=z,r=r,q=q,feedrate=feedrate)

def g83_gcode(x=None,
              y= None,
              z= None,
              r=None,
              q = None,
              feedrate=None):
    """ Peck drill"""
    if z==None or r==None:
        raise GcodeParameterError('G83 parameter error')
    if r<z:
        raise GcodeParameterError('G83 parameter error - r smaller than z')
    return gcode_format(prefix='G83 G98',x=x,y=y,z=z,r=r,q=q,feedrate=feedrate)


def g81_gcode(x=None,
              y= None,
              z= None,
              r=None,
              feedrate=None):
    """ Normal drill"""
    if z==None or r==None:
        raise GcodeParameterError('G81 parameter error')
    if r<z:
        raise GcodeParameterError('G81 parameter error - r smaller than z')
    return gcode_format(prefix='G81 G98',x=x,y=y,z=z,r=r,feedrate=feedrate)


########################################################################
#                           UTILITIES                                  #
########################################################################

def generate_heights(from_z=0.0,to_z=-1.0,step=-0.10):
    """Generator of Z heights, intended to be used in a for loop to mill down in steps.

    Keyword arguments:
    from_z -- starting height (default 0.0)
    to_z   -- end height (has to be below from_z) (default -1.0)
    step   -- the step by which the milling head goes from from_z to to_z (default -0.1)

    """
    if to_z is None or from_z is None or step is None:
        raise MissingParameterError('Missing parameter')

    if (from_z < to_z):
        raise WrongParameterError('we are supposed to mill down - altitude problem')
    
    if (step>=0):
        raise WrongParameterError('we are supposed to mill down - step problem')

    cur = float(from_z)
    
    while cur > to_z:
        yield cur
        cur += step
        
    yield to_z



def generate_excentric(start=0.0, end=1.0,tool_diameter=3.0):
    """Generator of Z excentric values, This function is intended 
    to be used in a for loop to mill outwards in steps of tool_diameter/2

    Keyword arguments:
    start           -- start position (default 0.0)
    end             -- end position (default 1.0)
    tool_diameter   -- tool diameter in mm (default 3.0)

    """
    if end<tool_diameter/2.0:
        raise WrongParameterError('cannot generate excentric dimensions')
    
    value = float(start) + float(tool_diameter /2.0)
    
    while value < end-tool_diameter/2.0:
        yield value 
        value +=tool_diameter/2.0
        
    yield end-tool_diameter/2.0


# 'C:/Users/guillaume/Dropbox'
def get_filepath(dir_='C:/',filename='gcode',extension='.ngc'):
    return os.path.join(os.path.realpath(dir_),filename+extension)


class Point:
    """Simple class that stores 2D coordinates for a point"""

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x,self.y+other.y)
    
    def __sub__(self, other):
        return Point(self.x-other.x,self.y-other.y)
        
    def offset(self, x,y):
        return Point(self.x + x, self.y +y)
        
    def rotate_around_origin(self, degrees):
        radians = math.pi /180 *degrees
        return Point(self.x*math.cos(radians) - self.y*math.sin(radians),  self.x*math.sin(radians)+self.y*math.cos(radians))
    
    def rotate(self, center, degrees):
        radians = math.pi /180 *degrees
        displacement = self - center
        point = Point(0,0)
        point.x = displacement.x * math.cos(radians) + displacement.y * math.sin(radians)
        point.y = displacement.y * math.cos(radians) - displacement.x * math.sin(radians)
        point = point + center
        return point

########################################################################
#                           EXCEPTIONS                                 #
########################################################################

class MissingParameterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class WrongParameterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GcodeParameterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

