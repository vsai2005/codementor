"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

/** Landing hero only (PRD 4.1). A slowly rotating wireframe icosahedron in ink
 *  on cream — flat, no lighting model, so it matches the design system rather
 *  than fighting it. Skipped entirely under prefers-reduced-motion. */
export function Hero3D() {
  const mount = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const node = mount.current;
    if (!node) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const width = node.clientWidth;
    const height = node.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
    camera.position.z = 3.2;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    node.appendChild(renderer.domElement);

    const geometry = new THREE.IcosahedronGeometry(1.25, 1);
    const mesh = new THREE.LineSegments(
      new THREE.WireframeGeometry(geometry),
      new THREE.LineBasicMaterial({ color: 0x14213d }),
    );
    scene.add(mesh);

    let frame = 0;
    const animate = () => {
      frame = requestAnimationFrame(animate);
      mesh.rotation.x += 0.0015;
      mesh.rotation.y += 0.0025;
      renderer.render(scene, camera);
    };
    animate();

    const onResize = () => {
      const w = node.clientWidth;
      const h = node.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", onResize);

    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("resize", onResize);
      renderer.dispose();
      geometry.dispose();
      node.removeChild(renderer.domElement);
    };
  }, []);

  return <div ref={mount} className="h-64 w-full sm:h-80" aria-hidden />;
}
