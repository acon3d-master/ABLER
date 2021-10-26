# Run this script to install dependencies needed by Abler.
# NOTE: Use the Python executable which is going to be packaged into Blender build.

import subprocess
import sys

deps = [
    "mixpanel==4.9.0",
]

subprocess.check_call([sys.executable, "-m", "pip", "install", " ".join(deps)])
