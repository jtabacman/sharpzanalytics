/**
 * Sharpz hero — 3D rotating graph built with Three.js.
 * ~600 nodes distributed via golden-spiral on a sphere + curved edges
 * between nearby nodes. Slow Y rotation + subtle X wobble + mouse parallax.
 * Background dust for depth.
 */

(function () {
  if (typeof THREE === 'undefined') {
    console.warn('[sharpz hero] Three.js not loaded');
    return;
  }

  const canvas = document.getElementById('three-canvas');
  if (!canvas) return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    60, window.innerWidth / window.innerHeight, 0.1, 1000
  );
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x0a0a0a, 1);
  camera.position.z = 55;

  const graphRoot = new THREE.Group();
  scene.add(graphRoot);

  // ---------- nodes ----------
  const NODE_COUNT = 600;
  const SPHERE_R = 28;
  const CLUSTER_COUNT = 12;
  const nodePositions = [];
  const hubIndices = new Set();

  // Golden-spiral sphere distribution
  const phi = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < NODE_COUNT * 0.7; i++) {
    const y = 1 - (i / (NODE_COUNT * 0.7 - 1)) * 2;
    const r = Math.sqrt(1 - y * y);
    const theta = phi * i;
    const x = Math.cos(theta) * r;
    const z = Math.sin(theta) * r;
    nodePositions.push(new THREE.Vector3(x * SPHERE_R, y * SPHERE_R, z * SPHERE_R));
  }

  // Inner cluster nodes (adds depth)
  for (let c = 0; c < CLUSTER_COUNT; c++) {
    const cx = (Math.random() - 0.5) * SPHERE_R * 1.2;
    const cy = (Math.random() - 0.5) * SPHERE_R * 1.2;
    const cz = (Math.random() - 0.5) * SPHERE_R * 1.2;
    const members = 10 + Math.floor(Math.random() * 8);
    const firstIdx = nodePositions.length;
    for (let k = 0; k < members; k++) {
      nodePositions.push(new THREE.Vector3(
        cx + (Math.random() - 0.5) * 6,
        cy + (Math.random() - 0.5) * 6,
        cz + (Math.random() - 0.5) * 6
      ));
    }
    hubIndices.add(firstIdx);      // first 2 per cluster are hubs
    hubIndices.add(firstIdx + 1);
  }

  // Loose scatter (rounds it out)
  while (nodePositions.length < NODE_COUNT) {
    const dir = new THREE.Vector3(
      Math.random() - 0.5,
      Math.random() - 0.5,
      Math.random() - 0.5
    ).normalize();
    const dist = SPHERE_R * (0.6 + Math.random() * 0.5);
    nodePositions.push(dir.multiplyScalar(dist));
  }

  // Point cloud
  const nodeGeom = new THREE.BufferGeometry();
  const nodePositionAttr = new Float32Array(NODE_COUNT * 3);
  const nodeSizeAttr = new Float32Array(NODE_COUNT);
  for (let i = 0; i < NODE_COUNT; i++) {
    nodePositionAttr[i * 3]     = nodePositions[i].x;
    nodePositionAttr[i * 3 + 1] = nodePositions[i].y;
    nodePositionAttr[i * 3 + 2] = nodePositions[i].z;
    nodeSizeAttr[i] = hubIndices.has(i) ? 3.2 : 1.6;
  }
  nodeGeom.setAttribute('position', new THREE.BufferAttribute(nodePositionAttr, 3));
  nodeGeom.setAttribute('aSize', new THREE.BufferAttribute(nodeSizeAttr, 1));

  const nodeMat = new THREE.ShaderMaterial({
    uniforms: { uPixelRatio: { value: renderer.getPixelRatio() } },
    transparent: true,
    depthWrite: false,
    vertexShader: `
      attribute float aSize;
      varying float vSize;
      uniform float uPixelRatio;
      void main() {
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = aSize * uPixelRatio * (260.0 / -mv.z);
        gl_Position = projectionMatrix * mv;
        vSize = aSize;
      }
    `,
    fragmentShader: `
      varying float vSize;
      void main() {
        vec2 uv = gl_PointCoord - 0.5;
        float d = length(uv);
        if (d > 0.5) discard;
        float a = smoothstep(0.5, 0.15, d);
        float brightness = 0.6 + vSize * 0.12;
        gl_FragColor = vec4(vec3(brightness), a * 0.9);
      }
    `,
  });
  graphRoot.add(new THREE.Points(nodeGeom, nodeMat));

  // ---------- edges ----------
  const EDGE_MAX_DIST = 14;
  const edgePoints = [];
  const edgeColors = [];
  const CURVE_SEGMENTS = 12;
  let edgeCount = 0;
  const MAX_EDGES = 1100;

  for (let i = 0; i < NODE_COUNT && edgeCount < MAX_EDGES; i++) {
    for (let j = i + 1; j < NODE_COUNT && edgeCount < MAX_EDGES; j++) {
      const dist = nodePositions[i].distanceTo(nodePositions[j]);
      if (dist > EDGE_MAX_DIST) continue;
      if (Math.random() > 0.25) continue;

      const a = nodePositions[i];
      const b = nodePositions[j];
      const mid = new THREE.Vector3().addVectors(a, b).multiplyScalar(0.5);
      // curve direction — some inward, some outward, some lateral
      const roll = Math.random();
      const bend = 2 + Math.random() * 4;
      if (roll < 0.35) {
        mid.multiplyScalar(0.75); // toward center
      } else if (roll < 0.60) {
        mid.multiplyScalar(1.18); // outward
      } else {
        mid.add(new THREE.Vector3(
          (Math.random() - 0.5) * bend,
          (Math.random() - 0.5) * bend,
          (Math.random() - 0.5) * bend
        ));
      }

      const curve = new THREE.QuadraticBezierCurve3(a, mid, b);
      const pts = curve.getPoints(CURVE_SEGMENTS);
      const isHubEdge = hubIndices.has(i) || hubIndices.has(j);
      const opacity = isHubEdge ? 0.38 : 0.15;
      for (let k = 0; k < pts.length - 1; k++) {
        edgePoints.push(pts[k].x, pts[k].y, pts[k].z);
        edgePoints.push(pts[k + 1].x, pts[k + 1].y, pts[k + 1].z);
        edgeColors.push(opacity, opacity, opacity);
        edgeColors.push(opacity, opacity, opacity);
      }
      edgeCount++;
    }
  }

  const edgeGeom = new THREE.BufferGeometry();
  edgeGeom.setAttribute('position', new THREE.Float32BufferAttribute(edgePoints, 3));
  edgeGeom.setAttribute('color', new THREE.Float32BufferAttribute(edgeColors, 3));

  const edgeMat = new THREE.LineBasicMaterial({
    vertexColors: true,
    transparent: true,
    opacity: 1.0,
    depthWrite: false,
  });
  graphRoot.add(new THREE.LineSegments(edgeGeom, edgeMat));

  // ---------- ambient dust ----------
  const DUST_COUNT = 400;
  const dustGeom = new THREE.BufferGeometry();
  const dustPos = new Float32Array(DUST_COUNT * 3);
  for (let i = 0; i < DUST_COUNT; i++) {
    dustPos[i * 3]     = (Math.random() - 0.5) * 140;
    dustPos[i * 3 + 1] = (Math.random() - 0.5) * 140;
    dustPos[i * 3 + 2] = (Math.random() - 0.5) * 140;
  }
  dustGeom.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
  const dustMat = new THREE.PointsMaterial({
    color: 0x888888,
    size: 0.7,
    transparent: true,
    opacity: 0.22,
    depthWrite: false,
  });
  const dust = new THREE.Points(dustGeom, dustMat);
  scene.add(dust);

  // ---------- mouse parallax ----------
  let mx = 0, my = 0;
  window.addEventListener('mousemove', (e) => {
    mx = (e.clientX / window.innerWidth - 0.5) * 2;
    my = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  // ---------- resize ----------
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  // ---------- animation loop ----------
  let t = 0;
  function animate() {
    t += 0.0012;
    graphRoot.rotation.y += 0.0012;
    graphRoot.rotation.x = Math.sin(t * 0.7) * 0.04;
    dust.rotation.y -= 0.0004;
    camera.position.x += (mx * 6 - camera.position.x) * 0.04;
    camera.position.y += (-my * 4 - camera.position.y) * 0.04;
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  animate();
})();
