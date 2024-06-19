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
        self._x = self._x + self._vX 
        self._y = self._y + self._vY 
    def draw_particle(self):
        circle(self._x, self._y, self._radius)

class Collisions:
    def update_vel_collision(self, p1, p2):
        pos_1, pos_2 = p1.get_pos(), p2.get_pos()
        rad_1, rad_2 = p1.get_radius(), p2.get_radius()
        dist = math.sqrt((pos_1[0] - pos_2[0])**2 + (pos_1[1] - pos_2[1])**2)
        if dist <= rad_1 + rad_2:
            m_1, m_2 = p1.get_mass(), p2.get_mass()
            v_1i, v_2i = p1.get_vel(), p2.get_vel()
            
            # Calculating the new velocities after collision
            v_1f_x = (v_1i[0] * (m_1 - m_2) + (2 * m_2 * v_2i[0])) / (m_1 + m_2)
            v_1f_y = (v_1i[1] * (m_1 - m_2) + (2 * m_2 * v_2i[1])) / (m_1 + m_2)
            v_2f_x = (v_2i[0] * (m_2 - m_1) + (2 * m_1 * v_1i[0])) / (m_1 + m_2)
            v_2f_y = (v_2i[1] * (m_2 - m_1) + (2 * m_1 * v_1i[1])) / (m_1 + m_2)
            
            p1.set_vel(v_1f_x, v_1f_y)
            p2.set_vel(v_2f_x, v_2f_y)

    def update_vel_wall(self, p):
        pos = p.get_pos()
        rad = p.get_radius()
        vel = p.get_vel()
        
        if pos[0] - rad <= 0:  # Left wall
            p.set_vel(-1 * vel[0], vel[1])
            p._x = rad  # Move particle inside the boundary
        elif pos[0] + rad >= w:  # Right wall
            p.set_vel(-1 * vel[0], vel[1])
            p._x = w - rad  # Move particle inside the boundary
            
        if pos[1] - rad <= 0:  # Top wall
            p.set_vel(vel[0], -1 * vel[1])
            p._y = rad  # Move particle inside the boundary
        elif pos[1] + rad >= h:  # Bottom wall
            p.set_vel(vel[0], -1 * vel[1])
            p._y = h - rad  # Move particle inside the boundary

class Button:
    def __init__(self, x, y, width, height, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
    
    def display(self):
        fill(0)
        rect(self.x, self.y, self.width, self.height)
        fill(255)
        textAlign(CENTER, CENTER)
        text(self.label, self.x + self.width / 2, self.y + self.height / 2)
    
    def is_clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

class Slider:
    def __init__(self, x, y, min_val, max_val, initial_val, label):
        self.x = x
        self.y = y
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
    
    def display(self):
        fill(0)
        line(self.x, self.y, self.x + 100, self.y)
        ellipse(self.x + self.map_val(self.val), self.y, 10, 10)
        textAlign(CENTER, CENTER)
        text(self.label + ": " + str(round(self.val, 2)), self.x + 50, self.y - 15)
    
    def map_val(self, val):
        return 100 * (val - self.min_val) / (self.max_val - self.min_val)
    
    def update(self, mouse_x):
        if self.x <= mouse_x <= self.x + 100:
            self.val = self.min_val + (mouse_x - self.x) * (self.max_val - self.min_val) / 100

# Set the height and width for the canvas
h = 600
w = 600
p1 = Particle(100, 100, 5, 5, 10, 10)
p2 = Particle(200, 200, 5, 5, 10, 10)
helpers = Collisions()
frame_index = 0

# Global variables for sliders and button
particles = []
add_particle_button = None
slider_start_x = None
slider_start_y = None
slider_vx = None
slider_vy = None
slider_mass = None
slider_radius = None

# Define the 'setup' function, which is called once when the program starts
def setup():
    global add_particle_button, slider_start_x, slider_start_y, slider_vx, slider_vy, slider_mass, slider_radius
    size(h, w)
    add_particle_button = Button(20, 550, 100, 30, "Add Particle")
    slider_start_x = Slider(150, 520, 0, w, w / 2, "Start X")
    slider_start_y = Slider(150, 550, 0, h, h / 2, "Start Y")
    slider_vx = Slider(300, 520, -10, 10, 0, "Velocity X")
    slider_vy = Slider(300, 550, -10, 10, 0, "Velocity Y")
    slider_mass = Slider(450, 520, 1, 20, 10, "Mass")
    slider_radius = Slider(450, 550, 5, 30, 15, "Radius")

# Define the 'draw' function, which is called continuously by Processing
def draw():
    background(255)
    add_particle_button.display()
    slider_start_x.display()
    slider_start_y.display()
    slider_vx.display()
    slider_vy.display()
    slider_mass.display()
    slider_radius.display()
    
    for particle in particles:
        helpers.update_vel_wall(particle)
        particle.update_pos()
        particle.draw_particle()
    
    if len(particles) > 1:
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                helpers.update_vel_collision(particles[i], particles[j])

def mouseClicked():
    global particles
    if add_particle_button.is_clicked(mouseX, mouseY):
        new_particle = Particle(
            slider_start_x.val, slider_start_y.val,
            slider_vx.val, slider_vy.val,
            slider_mass.val, slider_radius.val
        )
        particles.append(new_particle)
    
    sliders = [slider_start_x, slider_start_y, slider_vx, slider_vy, slider_mass, slider_radius]
    for slider in sliders:
        if slider.x <= mouseX <= slider.x + 100 and slider.y - 5 <= mouseY <= slider.y + 5:
            slider.update(mouseX)

def mouseDragged():
    sliders = [slider_start_x, slider_start_y, slider_vx, slider_vy, slider_mass, slider_radius]
    for slider in sliders:
        if slider.x <= mouseX <= slider.x + 100 and slider.y - 5 <= mouseY <= slider.y + 5:
            slider.update(mouseX)
