# reach-auto-fly (v1 — Archived)

> **Archived v1 prototype** from the original REACH project. Superseded by [`reach-core`](https://github.com/oc7o/reach-core) (Rust + gRPC + MAVLink) and [`reach-control`](https://github.com/oc7o/reach-control) (SwiftUI).

## Overview

Autonomous Python companion-computer stack built for an NVIDIA Jetson Nano connected to a Pixhawk 2.4.8 (ArduPilot) hexacopter:

- **Flight control (`src/reach/apps/flight_controller/`)** — DroneKit/MAVLink2 takeoff, waypoint navigation, relative movement, position hold, landing, and GPS telemetry broadcasts
- **Person recognition (`src/reach/apps/recognition/`)** — On-board person detection (SSD MobileNet V2) paired with clothing-color and feature extraction to locate a target person from a reference image
- **Communication (`src/reach/apps/mqtt/`)** — MQTT command/response and telemetry daemon (paired with the legacy Flutter ground station at `reach-control@v0.1-flutter-legacy`)
- **Emergency handling (`src/reach/apps/emergency/`)** — Fail-safe thread monitoring

## Model Weights

Pretrained model weights are not checked into this repository. To run the recognition module locally, download `ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8` from the TensorFlow 2 Detection Model Zoo and extract it into `src/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8/`.

## Configuration

Set `REACH_MQTT_BROKER` in your environment (or `.env`) to point to your Mosquitto broker (defaults to `127.0.0.1`).
