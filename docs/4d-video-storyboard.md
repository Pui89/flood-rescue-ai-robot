# Flood Rescue AI Robot — cinematic 4D concept

**Status:** storyboard and production prompt only; no rendered video or real-world capability is implied.

## 30-second sequence
1. **0–5 s — Establishing shot:** dawn after a monsoon, floodwater across a Thai neighborhood; camera glides low over rippling water toward the orange amphibious tracked robot.
2. **5–10 s — Hardware reveal:** slow 180° orbit, showing sealed hull, tracks, sensor mast, RGB-D camera and LiDAR housing; rain droplets and realistic reflections.
3. **10–17 s — Reconnaissance:** robot crawls through shallow moving water; sensor overlays briefly show a point cloud and a top-down occupancy map, clearly presented as visualization.
4. **17–24 s — Mission view:** operator tablet shows a tentative route, water-depth annotations and hazard markers; robot pauses at an obstacle rather than attempting an unsafe crossing.
5. **24–30 s — Hero shot:** camera cranes upward as the robot maps the flooded street; end card: “PUI89 Flood Rescue — Simulation-first robotics concept”.

## Video-generation prompt
Create a photorealistic, cinematic 3D robotics concept film, 16:9, 4K look, 24 fps, 30 seconds. Feature a compact orange-and-charcoal amphibious tracked flood-reconnaissance robot with sealed low-profile hull, visible rubber tracks, sensor mast, LiDAR and stereo/depth cameras. Thai monsoon environment, realistic water interaction, wet materials, physically plausible motion, restrained documentary lighting, slow dolly and orbit shots, crisp industrial design details. Add subtle transparent mapping graphics only during the sensor sequence. Keep the robot design consistent across all shots. No people in danger, no rescue outcome claims, no logos other than the final text title. The phrase “4D” here means a time-based animated 3D presentation; do not simulate haptics or claim a physical prototype exists.

## Suggested open-source workflow
- Blender: modeling, animation, camera, rendering.
- FreeCAD: mechanical layout and dimensioned parts.
- ROS 2 + Gazebo: later simulation integration, after a model and sensor configuration exist.
- Kdenlive: editing, titles and sound mix.

## Shot checklist
- [ ] Lock a consistent robot model and materials.
- [ ] Animate tracks and water with conservative physics.
- [ ] Render preview at 720p before final rendering.
- [ ] Label sensor overlays “illustrative simulation”.
- [ ] Publish final render only after it has actually been rendered and reviewed.
