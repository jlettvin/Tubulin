#!/usr/bin/env python

"""
You must run 'cd ../Paraboloid2; ./Paraboloid.py;' to generate data.
Then copy the new ../Paraboloid2/tubulin/tubulin.{timestamp} file
to {cwd}/tubulin and set the timestamp a few lines down to the above value.
Then run ./tubulin.py
"""

from cPickle import (load, dump)
from random import (seed, randint, random)
from math import (sqrt, ceil)
from itertools import (product)
from pprint import (pprint)
from scipy import (arange)

from Tag import TAG

timestamp = '201409212111'

class Paraboloid(object):
    """
    A set of x, y, z, r, and R values for points on a paraboloid surface
    """

    def __init__(self, rmax=10):
        self._genPoints(rmax)
        self._genLines()

    def radius(self, x, y):
        return sqrt(x**2+y**2)

    def distance(self, p1, p2):
        x1, y1, z1 = [p1[c] for c in 'xyz']
        x2, y2, z2 = [p2[c] for c in 'xyz']
        return sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)

    def _genPoints(self, rmax):
        self.r = set()
        self.ring = {}
        self.xyzrR = []
        # Could be done with comprehensions, but with inefficient r exclusions
        for x,y in product(arange(-rmax,+rmax+1), repeat=2):
            r = self.radius(x,y)
            if r > rmax:
                continue
            self.r.add(r)
            z = sqrt(r)
            R = sqrt(x**2+y**2+z**2)
            self.xyzrR += [{'x':x,'y':y,'z':z,'r':r,'R':R},]
            self.ring[r] = self.ring.get(r, [])+[self.xyzrR[-1],]
        self.r = sorted(self.r)
        pprint(self.ring)
        self.N = len(self.xyzrR) # tubulin strand count
        print 'tube count:', self.N
        # hN = Hex(self.N) # Temp!  Run generator to test it
        # h1000 = Hex(1000)

    def _genLines(self):
        pass

    def __str__(self):
        return str(self.xyzrR)+'\n'+str(self.r)

"""
def generate(r=10, dr=1):
    radii = [xyzrR(x,y) for x,y in product(range(-r,+r+dr,dr), repeat=2)]
    rs = set()
    for x,y,z,r,R in radii:
        rs.add(r)
    print radii
"""

def express_tubulin():
    R, T, tubulin = 3.0, [], {}

    xmax = 3.0
    scale = 0.3
    width = 0.002
    length = width * 10.0
    for k, V in tubulin.iteritems():
        T += [[], ]

        # One dendritic spine for each tubulin.
        tip = normit(V[0][0])
        # vertical = (0,0,1)
        # arrow(pos=tip, axis=vertical , color=color.red, length=length, shaftwidth=width)
        radial = (c * a for c, a in zip(tip, (1.0, 1.0, 0.0)))
        #radial = list(tip)
        #radial[2] = 0
        radial = tuple(radial)
        arrow(pos=tip, axis=radial , color=color.red, length=length, shaftwidth=width)

        # Follow tubulin down
        for v in V:
            T[-1] += [normit(v[0]), ]
        # An axon of sorts
        full = 2.0
        half = full / 2.0
        for i in range(4):
            while true:
                x, y = full * random() - half, full * random() - half
                if sqrt(x*x+y*y) <= 0.5:
                    T[-1] += [[x/15.0, y/15.0, -i/4.0], ]
                    break
        curve(pos=T[-1], radius=width, color=randcolor())
    dump(T, open("tubulin/simple.%s.p" % timestamp, "wb"))
    #print('Use right mouse button to rotate.')
    #while True:
        #key = scene.kb.getkey()
        #keyfun.get(key, noop)(key)

class Tree(object):

    def __init__(self, **kw):
        raw = kw.get('tubulin', None)
        pickle = kw.get('pickle', None)
        if raw:
            self.line = []
            with open(raw) as source:
                for line in source:
                    parts = line.strip().split(' ')
                    elements = parts[2:]
                    self.line += [[],]
                    for element in elements:
                        thing = element.strip()[1:-1].split(',')
                        x, y, z = [float(d) for d in element.strip()[1:-1].split(',')]
                        self.line[-1] += [[x/10, y/10, z/100],]
        elif pickle:
            self.line = load(open(pickle))

    def __call__(self, **kw):
        pass

    def tag_material(self, c, h):
        TAG.add('var %cmat = new THREE.LineBasicMaterial(' % (c))
        TAG.add('{color: 0x%06x, linewidth: 3}' % h)
        TAG.add(');\n')

    def tag_transientVectorSensors(self, L, geo, seg, point, scale=2e-2):
        x, y, z = point
        N = sqrt(x**2+y**2)
        Rgeo = 'var R%s = new THREE.Geometry();\n' % (geo)
        Ggeo = 'var G%s = new THREE.Geometry();\n' % (geo)
        Rseg = 'seg_R%d' % (L)
        Gseg = 'seg_G%d' % (L)
        TAG.add(Rgeo+Ggeo+'\n')

        TAG.add('R%s.vertices.push(' % (geo))
        TAG.add('new THREE.Vector3(%f,%f,%f)' % (x,y,z))
        TAG.add(',new THREE.Vector3(%f,%f,%f)' % (x,y,z+scale))
        TAG.add(');\n')

        XN, YN = scale*x/N, scale*y/N
        TAG.add('G%s.vertices.push(' % (geo))
        TAG.add('new THREE.Vector3(%f,%f,%f)' % (x,y,z))
        TAG.add(',new THREE.Vector3(%f,%f,%f)' % (x+XN,y+YN,z))
        TAG.add(');\n')

        TAG.add('var R%s = new THREE.Line(R%s,Rmat);\n' % (seg, geo))
        TAG.add('scene.add(R%s);\n' % (seg))

        TAG.add('var G%s = new THREE.Line(G%s,Gmat);\n' % (seg, geo))
        TAG.add('scene.add(G%s);\n' % (seg))

    def tag_nl(self):
        TAG.add('\n')

    def tag_tubulin(self, L, line):
        mat = 'mat_%d' % (L)
        geo = 'geo_%d' % (L)
        seg = 'seg_%d' % (L)

        TAG.add('var %s = new THREE.LineBasicMaterial(' % (mat))
        value = randint(0, 0xffffff)
        TAG.add('  {color: 0x%06x, linewidth: 3}' % (value))
        TAG.add(');\n')

        TAG.add('var %s = new THREE.Geometry();\n' % (geo))

        TAG.add('%s.vertices.push(' % (geo))
        comma = ''
        for S, segment in enumerate(line):
            X, Y, Z = segment
            TAG.add('%snew THREE.Vector3(%f,%f,%f)' % (comma,X,Y,Z))
            comma = ','
        TAG.add(');\n')
        TAG.add('var %s = new THREE.Line(%s,%s);\n' % (seg, geo, mat))
        TAG.add('scene.add(%s);\n' % (seg))
        TAG.add('\n')
        point = line[0]
        self.tag_transientVectorSensors(L, geo, seg, point)

    def tagged(self):
        ini = """
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth/window.innerHeight,
    0.1,
    1000);

var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

camera.position.z = 2;
camera.position.y = 1;
camera.position.x = 1;

var rotSpeed = 2e-3;

function checkRotation() {
    var x = camera.position.x,
        y = camera.position.y,
        z = camera.position.z;
    camera.position.x = x * Math.cos(rotSpeed) + z * Math.sin(rotSpeed);
    camera.position.z = z * Math.cos(rotSpeed) - x * Math.sin(rotSpeed);
    camera.lookAt(scene.position);
};

var render = function () {
    requestAnimationFrame(render);
    checkRotation();
    renderer.render(scene, camera);
};

render();
"""

        with TAG('html'):
            with TAG('head'):
                with TAG('style'):
                    TAG.add("canvas { width: 100%; height: 100%; }\n")
            with TAG('body'):
                with TAG('script', src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js"):
                    pass
                with TAG('script', src="http://cdnjs.cloudflare.com/ajax/libs/three.js/r68/three.min.js"):
                    pass
                with TAG('script'):
                    self.tag_material('R', 0xff0000)
                    self.tag_material('G', 0x00ff00)
                    TAG.add(ini)
                    for N, line in enumerate(self.line):
                        self.tag_tubulin(N, line)
                    TAG.add("render();\n")
                pass

        return TAG.final()

seed()
paraboloid = Paraboloid(3)
#print paraboloid
express_tubulin()
tree = Tree(tubulin='tubulin/tubulin.20140921213045') #, pickle='simple.20140330221624.p')
with open('bipolar.shared.path.html', 'w') as target:
    print>>target, tree.tagged()
