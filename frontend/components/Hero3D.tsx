"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

import { useTheme } from "@/lib/useTheme";

/** Landing hero (Phase 5). A rotating wireframe icosahedron adapting to theme.
 *  Skipped entirely under prefers-reduced-motion. */
export function Hero3D() {
  const mount = useRef<HTMLDivElement>(null);
  const { theme } = useTheme();

  useEffect(() => {
    const node = mount.current;
    if (!node) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const width = node.clientWidth || 320;
    const height = node.clientHeight || 256;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
    camera.position.z = 3.2;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    node.appendChild(renderer.domElement);

    const geometry = new THREE.IcosahedronGeometry(1.25, 1);
    const wireframe = new THREE.WireframeGeometry(geometry);
    const materialColor = theme === "dark" ? 0x93c5fd : 0x14213d;
    const material = new THREE.LineBasicMaterial({ color: materialColor });
    const mesh = new THREE.LineSegments(wireframe, material);
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
      if (!node) return;
      const w = node.clientWidth;
      const h = node.clientHeight;
      if (w === 0 || h === 0) return;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", onResize);

    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("resize", onResize);
      material.dispose();
      wireframe.dispose();
      geometry.dispose();
      renderer.dispose();
      if (node.contains(renderer.domElement)) {
        node.removeChild(renderer.domElement);
      }
    };
  }, [theme]);

  return <div ref={mount} className="h-64 w-full sm:h-80" aria-hidden />;
}
