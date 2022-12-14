# The simulator of the system with particles that constantly rotate around a central point with const speed

from matplotlib import pyplot as plt 
from matplotlib import animation 
from random import uniform 

# we accept positive and negative numbers for all params; the sign of ang_vel determines the direction of roatation
class Particle:
    def __init__(self, x, y, ang_vel): 
        self.x = x 
        self.y = y 
        self.ang_vel = ang_vel 


# The laws of motion (changing the part position over time)
class ParticleSimulator:
    def __init__(self, particles):
        self.particles = particles 

    def evolve(self, dt):
        timestep = 0.00001 
        nsteps = int(dt/timestep)

        for i in range(nsteps):
            for p in self.particles:
                # 1. calculate the direction 
                norm = (p.x**2 + p.y**2)**0.5 

                v_x = - p.y/norm 
                v_y = p.x/norm 

                # 2. calculate the displacement 
                d_x = timestep * p.ang_vel * v_x 
                d_y = timestep * p.ang_vel * v_y 

                p.x += d_x 
                p.y += d_y 
                # 3. repeat for all the time steps 


# Visualizing the simulation 

def visualize(simulator):

    X = [p.x for p in simulator.particles]
    Y = [p.y for p in simulator.particles] 

    fig = plt.figure()
    ax = plt.subplot(111, aspect='equal')
    line, = ax.plot(X, Y, 'ro')

    # Axis limits 
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    # It will be run when the animation starts 
    def init(): 
        line.set_data([], [])
        return line, # The comma is important! 

    def animate(i):
        # We let the particle evolve for 0.01 time units 
        simulator.evolve(0.01)
        X = [p.x for p in simulator.particles]
        Y = [p.y for p in simulator.particles]

        line.set_data(X, Y)
        return line, 

    # Call the animate function each 10 ms 
    anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True, interval=10)
    plt.show() 


# Test the code 

def test_visualize():
    particles = [ 
        Particle(0.3, 0.5, 1),
        Particle(0.0, -0.5, -1),
        Particle(-0.5, -0.4, 3)
    ]

    simulator = ParticleSimulator(particles) 
    visualize(simulator) 

# Unit test implementation 

def test_evolve():
    particles = [ 
        Particle(0.3, 0.5, +1),
        Particle(0.0, -0.5, -1),
        Particle(-0.1, -0.4, +3)
    ]
    
    simulator = ParticleSimulator(particles)

    simulator.evolve(0.1)

    p0, p1, p2 = particles 

    def fequal(a, b, eps=1e-5): 
        return abs(a - b) < eps 

    assert fequal(p0.x, 0.210269)
    assert fequal(p0.y, 0.543863)

    assert fequal(p1.x, -0.099334)
    assert fequal(p1.y, -0.490034)

    assert fequal(p2.x, 0.191358)
    assert fequal(p2.y, -0.365227)


# benchmark is a simple and representative use case that can be run to assess the running time of an application

def benchmark():
    # instantiate a thousand Particle objects with random coordinates and angular velocity
    particles = [ 
        Particle(uniform(-1.0, 1.0), uniform(-1.0, 1.0), uniform(-1.0, 1.0))
        for i in range(1000)
        ]

    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1) 

# Timing the benchmark through the Unix time command 
# $ time python3 particle_simulator.py 
# real: the actual time spent running from start to finish; includes I/O operations
# user: the cumulative time spent by all CPUs during the computation
# sys: the cumulative time spent by the CPUs during system-related tasks (memory allocation)

# Another way of timing the benchmark is throug python timeit module (used in IPython terminal)
"""" 
$ ipython
In [1]: from simul import benchmark
In [2]: %timeit benchmark()
"""

# Using the script 
# import timeit 
# result = timeit.repeat('benchmark()', setup='from __main__ import benchmark', number=10, repeat=3)






#if __name__ == '__main__':
 #   benchmark()

            