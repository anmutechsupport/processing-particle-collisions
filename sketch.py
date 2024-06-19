import math 

class Particle:
    def __init__(self, startX, startY, vX, vY, mass, radius):
        self._x = startX
        self._y = startY
        self._vX = vX
        self._vY = vY
        self._mass = mass
        self._radius = radius
    def get_pos(self):
        return (self._x, self._y)
    def get_vel(self):
        return (self._vX, self._vY)
    def get_radius(self):
        return self._radius
    def set_vel(self, vX, vY):
        self._vX = vX
        self._vY = vY
    def get_mass(self):
        return self._mass
    def update_pos(self):
        # dt is implicit in framerate
        self._x = self._x + self._vX 
        self._y = self._y + self._vY 
    def draw_particle(self):
        circle(self._x, self._y, self._radius)

class Collisions:
    def update_vel_collision(self, p1, p2):
        pos_1, pos_2 = p1.get_pos(), p2.get_pos()
        rad_1, rad_2 = p1.get_radius(), p2.get_radius()
        if ((pos_1[0] >= pos_2[0]-rad_2 or pos_1[0] <= pos_2[0]+rad_2) and (pos_1[1] >= pos_2[1]-rad_2 or pos_1[1] <= pos_2[1]+rad_2)) or ((pos_2[0] >= pos_1[0]-rad_1 or pos_2[0] <= pos_1[0]+rad_1) and (pos_2[1] >= pos_1[1]-rad_1 or pos_2[1] <= pos_1[1]+rad_1)):
            m_1, m_2 = p1.get_mass(), p2.get_mass()
            v_1i, v_2i = p1.get_vel(), p2.get_vel()
            v_1f = (
                (m_1 * v_1i[0] + m_2 * (2*v_2i[0]-v_1i[0]))/(m_1 + m_2),
                (m_1 * v_1i[1] + m_2 * (2*v_2i[1]-v_1i[1]))/(m_1 + m_2)
            )
            v_2f = (
                v_1i[0] - v_2i[0] + v_1f[0],
                v_1i[1] - v_2i[1] + v_1f[1]
            )
            p1.set_vel(v_1f[0], v_1f[1])
            p2.set_vel(v_2f[0], v_2f[1])

    def update_vel_wall(self, p):
        pos = p.get_pos()
        rad = p.get_radius()
        vel = p.get_vel()
        if pos[0]-rad <= 0 or pos[0]+rad >= w:
            p.set_vel(-1*vel[0], vel[1])
        if pos[1]-rad <= 0 or pos[1]+rad >= h:
            p.set_vel(vel[0], -1*vel[1])

# Set the height and width for the canvas
h = 600
w = 600
p1 = Particle(100, 100, 5, 5, 10, 10)
p2 = Particle(200, 200, -1, 1, 10, 10)
helpers = Collisions()
frame_index = 0

# Define the 'setup' function, which is called once when the program starts
def setup():
    
    # Set the size of the canvas using the global 'h' and 'w' vars
    size(h, w)  
    fill(255, 0, 0)
    stroke(255, 0, 0)
    p1.draw_particle()
    p2.draw_particle()



# Define the 'draw' function, which is called continuously by Processing
def draw():
    # Set the background color to white
    background(255)
    helpers.update_vel_wall(p1)
    helpers.update_vel_wall(p2)
    helpers.update_vel_collision(p1, p2)
    p1.update_pos()
    p2.update_pos()
    p1.draw_particle()
    p2.draw_particle()


# Define a function that's called whenever the mouse is clicked
def mouseClicked():
    pass

# Define a function that's called whenever the mouse is dragged
def mouseDragged():
    pass
