#!/bin/bash
set -evx

mkdir ~/.curvecore

# safety check
if [ ! -f ~/.curvecore/.curve.conf ]; then
  cp share/curve.conf.example ~/.curvecore/curve.conf
fi
