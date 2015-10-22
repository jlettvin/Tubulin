#!/usr/bin/env python

HEAD = """\
<!doctype html>
<html>
  <head>
   <title>Retinal Bipolar Tubulin Polymers</title>
   <style>
canvas{width:100%;height:100%;}
#stats{position:absolute;bottom:0;left:0;}
   </style>
   <script
    src="http://cdnjs.cloudflare.com/ajax/libs/stats.js/r14/Stats.min.js">
   </script>
   <script
    src="http://cdnjs.cloudflare.com/ajax/libs/three.js/r73/three.min.js">
   </script>
   <script
    src="http://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0-alpha1/jquery.min.js">
   </script>
  </head>
"""

BODY = """\
  <body>
    <canvas id="canvas"></canvas>
    <div align="center"><big><big><big>
    Dendritic Tubulin in One Retinal Bipolar Species
    </big></big></big><br />
    %s<br />
    <small><small><small>
    Copyright(c)2013-2015 Jonathan D. Lettvin, All Rights Reserved.
    </small></small></small>
    </div>
    <table align="center" border="1"><tr><td>
    <small><small><small>
    <ul>
    <li><i>You need a WebGL-enabled browser to see this.</i></li>
    <li>Tubulin strand tips are at cartesian paraboloid vertices.</li>
    <li>Tubulin polymers are shown coursing from dendritic spines to axon.</li>
    <li>Each tubulin polymer is given a relatively unique color.</li>
    <li>Not shown here is a required tgv subset activating "selector".</li>
    <li><b>
    &larr;
    &darr;
    &uarr;
    &rarr;
    change rotation speeds.
    &lt;SPACE&gt; toggles motion.
    </b></li>
    </ul>
    </small></small></small>
    </td><td>
    <small><small><small>
    <ul>
    <li>This shape has had a horizontal selector applied.</li>
    <li>Dentritic spines act as tgvs (transient gradient vector sensors).</li>
    <li>Active dendritic spines are the tiny green and red arrows.</li>
    <li>green/red (radial/axial) tgvs detect increases in oppositions.</li>
    <li>A sensed gradient becomes a signal coursing down a white tubulin.</li>
    <li>Legacy Paraboloid2/Tubulin.py generates the raw data</li>
    </ul>
    </small></small></small>
    </td></tr></table>
"""

CODE = """\
    <script>
        var scene = new THREE.Scene();
        var wPct = 0.95, hPct = 0.70;
        var width = window.innerWidth * wPct;
        var height = window.innerHeight * hPct;
        var camera = new THREE.PerspectiveCamera(100, width/height, 0.1, 1000);
        var spin = 1.0;
        var step = 0;

        var canvas   = document.getElementById('canvas'); 
        var renderer = new THREE.WebGLRenderer({canvas:canvas,antialias:true});
        var stats = new Stats();

        renderer.setSize(width, height);
        document.body.appendChild(renderer.domElement);
        document.body.appendChild(stats.domElement);

        canvas.width = width; canvas.height = height;
        renderer.setViewport(0, 0, canvas.clientWidth, canvas.clientHeight);

        camera.position.z = 1;
        camera.position.y = 1;
        camera.position.x = 1;

        var rotX = 0e-3, rotY = 5e-3, rotZ = 0e-3;

        function onWindowResize() {
          width  = window.innerWidth * wPct;
          height = window.innerHeight * hPct;
          camera.aspect = width / height;
          camera.updateProjectionMatrix();
          renderer.setSize(width, height);
        }

        function reverseRot() { rotX = -rotX; rotY = -rotY; rotZ = -rotZ; }

        function performRot() {
            var x = camera.position.x,
                y = camera.position.y,
                z = camera.position.z;
            var temp = spin;
            if(step > 0) { spin = 1.0; } /************************************/
            var rX = spin * rotX, rY = spin * rotY, rZ = spin * rotZ;
            var cosX = Math.cos(rX), sinX = Math.sin(rX); /*******************/
            camera.position.y = z * sinX + y * cosX;
            camera.position.z = z * cosX - y * sinX;
            var cosY = Math.cos(rY), sinY = Math.sin(rY); /*******************/
            camera.position.x = z * sinY + x * cosY;
            camera.position.z = z * cosY - x * sinY;
            // var cosZ = Math.cos(rZ), sinZ = Math.sin(rZ); /****************/
            // camera.position.x = y * sinZ + x * cosZ;
            // camera.position.y = y * cosZ - x * sinZ;
            if(step > 0) { spin = temp; step--; } /***************************/
            camera.lookAt(scene.position);
        } 

        function onDocumentKeyDown(event) { 
            event.preventDefault();
            // Get the key code of the pressed key (using vi bindings)
            switch (event.which) {
                case 32: spin = (spin == 1.0) ? 0.0 : 1.0; break; //     SPACE
                case 45: case 82: case 114: reverseRot();  break; //     -,R,r
                case 37: case 72: case 104: rotX -= 1e-3;  break; //  left,H,h
                case 40: case 74: case 106: rotY += 1e-3;  break; //  down,J,j
                case 38: case 75: case 107: rotY -= 1e-3;  break; //    up,K,k
                case 39: case 76: case 108: rotX += 1e-3;  break; // right,L,l
                case 13: case 83: case 115: step = 10;     break; // ENTER,S,s
                default:                                   break;
            }
        }

        document.addEventListener("keydown", onDocumentKeyDown, false);
        window.addEventListener('resize', onWindowResize, false);
"""

TAIL = """
      var render = function () {
        stats.update();
        requestAnimationFrame(render);
        performRot();
        renderer.render(scene, camera);
      };

      render();
    </script>
  </body>
</html>
"""

TEMP = """
      var material = new THREE.LineBasicMaterial(
          {color: 0x0000ff, linewidth: 2});
      var geometry = new THREE.Geometry();
      geometry.vertices.push(
              new THREE.Vector3( -2, -2, -2 ),
              new THREE.Vector3( +2, +2, +2 )
      );
      var line = new THREE.Line( geometry, material );
      scene.add( line );
"""

#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Common'))
#sys.path.append('..')

from cPickle import (load)
from random import (seed, randint)
from math import (sqrt)
from datetime import datetime

import Tag

class Tree(object):

    def __init__(self, **kw):
        self.timestamp = datetime.now().isoformat()
        tubulin = kw.get('tubulin', None)
        pickle = kw.get('pickle', None)
        self.color = {}
        self.seg = {}
        if pickle:
            #self.line = []
            self.line = load(open(pickle))
            #for strand in tubulin:
                #self.line += [[],]
                #for segment in strand:
                    #print segment
                ##print strand
                ##print '-'*70
                #pass
        elif tubulin:
            self.line = [[[-1,-1,-1], [+1,+1,+1], [-3,0,0]],]
            with open(tubulin) as source:
                for line in source:
                    element = line.split(' ')
                    assert element[0] == 'tubulin', element[0]
                    number = int(element[1][:-1])
                    triples = element[2:] #.reverse()
                    if not triples:
                        continue
                    self.line += [[],]
                    for triple in triples:
                        triple = triple.strip()
                        if not triple:
                            continue
                        triple = [float(f) for f in triple[1:-1].split(',')]
                        self.line[-1] += [triple,]
        self.Rmat = 'var Rmat = new THREE.LineBasicMaterial('
        self.Rmat += '{color: 0xff0000, linewidth: 4}'
        self.Rmat += ');\n'
        self.Gmat = 'var Gmat = new THREE.LineBasicMaterial('
        self.Gmat += '{color: 0x00ff00, linewidth: 4}'
        self.Gmat += ');\n'
        self.Imat = 'var Imat = new THREE.LineBasicMaterial('
        self.Imat += '{color: 0x777777, linewidth: 2}'
        self.Imat += ');\n'

        self.ring, self.margin = 0.75, 0.010117
        self.lower, self.upper = self.ring-self.margin, self.ring+self.margin

    def __call__(self, **kw):
        pass

    def rule(self, **kw):
        N = kw.get('N', 77)
        text = '//'
        text += '-'*N
        text += '\n'
        return text

    def tubulin(self, L, line):
        text = ''
        mat = 'mat_%d' % (L)
        geo = 'geo_%d' % (L)
        seg = 'seg_%d' % (L)

        x, y, z = point = line[0]  # Outermost point
        radius = sqrt(x**2+y**2)
        xy = "%f,%f" % (x, y)
        active = (radius >= self.lower and radius <= self.upper)

        # tubulin strands: one color per spine radius
        self.color[radius] = self.color.get(
                radius,
                [randint(0, 0x7f) for _ in range(3)])

        if active:
            (R, G, B), W = [0xff] * 3, 4
            print "tubulin: %10.10e" % (radius),
        else:
            (R, G, B), W = self.color[radius], 2

        text += 'var %s = new THREE.LineBasicMaterial(' % (mat)
        text += '  {color: 0x%02x%02x%02x, linewidth: %d}' % (R, G, B, W)
        text += ');\n'

        text += 'var %s = new THREE.Geometry();\n' % (geo)

        text += '%s.vertices.push(' % (geo)
        comma = ''

        for S, segment in enumerate(line):
            x, y, z = segment
            text += '%snew THREE.Vector3(%f,%f,%f)' % (comma,x, y, z)
            comma = ','

        text += ');\n'
        text += 'var %s = new THREE.Line(%s,%s);\n' % (seg, geo, mat)
        text += 'scene.add(%s);\n' % (seg)
        text += '\n'

        self.seg[radius] = self.seg.get(radius, {xy: seg})
        #self.seg[radius][xy] = seg  # Group segments of a radius indexed by xy

        return text, geo, seg

    def transientVectorSensors(self, L, geo, seg, point, scale=3e-2):
        text = ''
        x, y, z = point
        radius = sqrt(x**2+y**2)

        active = (radius >= self.lower and radius <= self.upper)

        Rgeo = 'var R%s = new THREE.Geometry();\n' % (geo)
        Ggeo = 'var G%s = new THREE.Geometry();\n' % (geo)
        Rseg = 'seg_R%d' % (L)
        Gseg = 'seg_G%d' % (L)
        text += Rgeo+Ggeo

        text += 'R%s.vertices.push(' % (geo)
        text += 'new THREE.Vector3(%f,%f,%f)' % (x,y,z)
        text += ',new THREE.Vector3(%f,%f,%f)' % (x,y,z+scale)
        text += ');\n'

        XN, YN = scale*x/radius, scale*y/radius
        text += 'G%s.vertices.push(' % (geo)
        text += 'new THREE.Vector3(%f,%f,%f)' % (x,y,z)
        text += ',new THREE.Vector3(%f,%f,%f)' % (x+XN,y+YN,z)
        text += ');\n'

        if active:
            R, G = ('R', 'G')
            print "  spine: %10.10e (R,G)" % (radius)
        else:
            R, G = ('I', 'I')

        text += 'var R%s = new THREE.Line(R%s,%cmat);\n' % (seg, geo, R)
        text += 'scene.add(R%s);\n' % (seg)

        text += 'var G%s = new THREE.Line(G%s,%cmat);\n' % (seg, geo, G)
        text += 'scene.add(G%s);\n' % (seg)

        return text

    def __str__(self):
        self.body = ''
        self.body += HEAD
        self.body += BODY % (self.timestamp)
        self.body += CODE
        self.body += self.Rmat+self.Gmat+self.Imat;
        for L, line in enumerate(self.line):
            text, geo, seg = self.tubulin(L, line)
            self.body += text
            self.body += self.transientVectorSensors(L, geo, seg, line[0])
            self.rule(N=77)
        self.body += TAIL
        return self.body

seed()
tree = Tree(tubulin='tubulin.20140330221624', pickle='simple.20140330221624.p')
with open('bipolar.unique.path.html', 'w') as target:
    print>>target, tree
