#!/bin/bash

xhost +local:root

docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --privileged \
  ghcr.io/saadiinho/lorenz_attractor:latest

xhost -local:root

