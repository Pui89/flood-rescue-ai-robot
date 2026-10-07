# Flood Rescue Research Dataset Specification

## Purpose

Create a benchmark that captures the conditions that cause rescue robots to fail, not only clean images.

## Sensor record

Each synchronized sample should include:
- RGB / stereo / RGB-D;
- thermal;
- LiDAR;
- IMU and odometry;
- GNSS/RTK when available;
- timestamp and synchronization quality;
- calibration/version IDs;
- robot pose and coordinate frame.

## Labels

### People
- visible person;
- partially occluded person;
- submerged/partially submerged person where ethically and legally collected;
- person in vehicle/structure;
- uncertain human-like object;
- no-person hard negative.

### Hazards
- floating debris;
- submerged obstacle;
- current/fast-water region;
- unstable structure;
- electrical hazard indicator;
- blocked passage;
- vehicle;
- vegetation;
- unknown/OOD object.

### Ground truth
- 2D/3D position;
- track ID;
- visibility/occlusion;
- object state;
- hazard severity;
- route traversability;
- rescue outcome;
- reason for failure when applicable.

## Scenario metadata

Record:
- weather;
- daylight/night;
- water condition;
- terrain;
- visibility;
- communication quality;
- GNSS availability;
- sensor failures;
- robot battery/load;
- scenario seed.

## Ethics and privacy

Human data must be collected with appropriate consent, institutional/operational authorization, privacy controls and secure retention. Synthetic or staged victim scenarios should be used where real-person collection is not appropriate.

## Dataset splits

Use:
- training;
- validation;
- same-environment test;
- unseen-environment test;
- severe-degradation test;
- OOD challenge set.

Do not leak frames from the same sequence across train/test.
