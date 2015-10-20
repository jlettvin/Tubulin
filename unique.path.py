#!/usr/bin/env python

HEAD = """<!doctype html>
<html>
  <head>
                <title>Retinal Bipolar Tubulin Polymers</title>
                <style>canvas { width: 100%; height: 100% }</style>
  </head>
  <body>
    <div align="center"><big><big><big>
    Dendritic Tubulin in One Retinal Bipolar Species
    </big></big></big><br />
    <small><small><small>
    Copyright(c)2013-2015 Jonathan D. Lettvin, All Rights Reserved.
    </small></small></small>
    </div>
    <table align="center" border="1"><tr><td>
    <small><small><small>
    <ul>
    <li><i>You need a WebGL-enabled browser to see this.</i></li>
    <li>The general shape is a paraboloid shell.</li>
    <li>Tubulin strand tips are at rectangular mesh vertices.</li>
    <li>Tubulin polymers are shown coursing from dendritic spines to axon.</li>
    <li>Each tubulin polymer is given a relatively unique color.</li>
    <li>Not shown here is a required tgv subset activating "selector".</li>
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
    <script
        src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js">
    </script>
    <script
        src="http://cdnjs.cloudflare.com/ajax/libs/three.js/r68/three.min.js">
    </script>
    <script>
        var scene = new THREE.Scene();
        var width = window.innerWidth * 0.98;
        var height = window.innerHeight * 0.75;
        var ratio = width / height;
        var camera = new THREE.PerspectiveCamera(75, ratio, 0.1, 1000);
        var useKeyboard = true;

        var renderer = new THREE.WebGLRenderer();
        renderer.setSize(width, height);
        document.body.appendChild(renderer.domElement);

        camera.position.z = 1;
        camera.position.y = 1;
        camera.position.x = 1;

        var rotSpeed = 5e-3;
        var dx = 0.0;
        var dy = 0.0;
        var dz = 0.0;

        function checkRotation(){
            var x = camera.position.x,
                y = camera.position.y,
                z = camera.position.z;

            if (useKeyboard) {
                if (dx > 0.0) {
                    camera.position.x =
                        x * Math.cos(rotSpeed) + z * Math.sin(rotSpeed);
                    camera.position.z =
                        z * Math.cos(rotSpeed) - x * Math.sin(rotSpeed);
                } else if (dx < 0.0) {
                    camera.position.x =
                        x * Math.cos(rotSpeed) - z * Math.sin(rotSpeed);
                    camera.position.z =
                        z * Math.cos(rotSpeed) + x * Math.sin(rotSpeed);
                }
                dx = 0.0;
            } else {
                camera.position.x =
                    x * Math.cos(rotSpeed) + z * Math.sin(rotSpeed);
                camera.position.z =
                    z * Math.cos(rotSpeed) - x * Math.sin(rotSpeed);
            }

            camera.lookAt(scene.position);

        } 

        function onDocumentKeyDown(event) { 
            // Get the key code of the pressed key 
            var keyCode = event.which;
            if        (keyCode==38) {  // up
            } else if (keyCode==40) {  // down
            } else if (keyCode==37 || keyCode==72 || keyCode==104) {  // left
                dx =  1.0;
            } else if (keyCode==40 || keyCode==76 || keyCode==108) {  // right
                dx = -1.0;
            }
        }

        document.addEventListener("keydown", onDocumentKeyDown, false);
"""

TAIL = """
      var render = function () {
              requestAnimationFrame(render);
              checkRotation();
              renderer.render(scene, camera);
      };

      render();
    </script>
    %s
  </body>
</html>
"""

BODY = """
      var material = new THREE.LineBasicMaterial(
          {color: 0x0000ff, linewidth: 3});
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
        self.Rmat += '{color: 0xff0000, linewidth: 7}'
        self.Rmat += ');\n'
        self.Gmat = 'var Gmat = new THREE.LineBasicMaterial('
        self.Gmat += '{color: 0x00ff00, linewidth: 7}'
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
        active = (radius >= self.lower and radius <= self.upper)

        if active:
            (R, G, B), W = [0xff] * 3, 7
            print "tubulin: %10.10e" % (radius)
        else:
            (R, G, B), W = [randint(0, 0x7f) for _ in range(3)], 2

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
        self.body += self.Rmat+self.Gmat+self.Imat;
        for L, line in enumerate(self.line):
            text, geo, seg = self.tubulin(L, line)
            self.body += text
            self.body += self.transientVectorSensors(L, geo, seg, line[0])
            self.rule(N=77)
        self.body += TAIL % (self.timestamp)
        return self.body

seed()
tree = Tree(tubulin='tubulin.20140330221624', pickle='simple.20140330221624.p')
with open('bipolar.unique.path.html', 'w') as target:
    print>>target, tree
