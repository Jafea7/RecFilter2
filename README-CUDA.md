---
Information regarding getting RecFilter v2 to use an NVIDIA GPU.
---

**Credits to @Datahell for working all this out.**

---

## Requirement:

Python 3.7.9 -> 3.9.6 - Has been tested on 3.7.9 and 3.9.5

A NVIDIA GPU with CUDA.

---

## Installation:

**RecFilter2 and NudeNet:**

Clone/download the repo, extract to a directory, then open a console/terminal within that directory.

Install the dependencies by entering:
```
pip install -r requirements.txt
```
or
```
python -m pip install -r requirements.txt
```

If you are running Python 3.8/3.9 on Windows 10 then open a console and enter the following commands:

```
python -m pip uninstall protobuf
python -m pip install protobuf
```

This will ensure you are using the latest version of `protobuf` which fixes a bug with running slow on Windows 10.

**CUDA Drivers:**

Make sure you have the latest nVida GFX drivers for your card installed.

Install the latest version of the [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) available from NVIDIA.

Install the latest version of the cuDNN libraries, this requires registering for a [NVIDIA Developer account](https://developer.nvidia.com/), (free).

Go to [cuDNN download](https://developer.nvidia.com/rdp/cudnn-download), you will need to login, agree to the license, then select your download.

**NOTE:** It gives a download for `Windows (x86)` but it's actually `Windows (x64)` libraries.

Install the cuDNN as per the instructions: [cuDNN Installation Guide](https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html)

Reboot your computer.

**Additional Python Modules:**

Open a console/terminal:

We need to replace `onnxruntime` with `onnxruntime-gpu` to utilise CUDA:
```
python -m pip uninstall -y onnxruntime
python -m pip install onnxruntime-gpu
```
We need to install the TensorFlow modules to convert the model:
```
python -m pip install tensorflow-gpu
python -m pip install tf2onnx
```

**Conversion of the onnx model**

Download the NudeNet detector checkpoint archive, [NudeNet Detector Checkpoint](https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_default_checkpoint_tf.tar), and extract to a directory.

Find the file `detector_v2_default_checkpoint.onnx` on your system, for Windows this will be:

`C:\Users\<username>\.NudeNet\detector_v2_default_checkpoint.onnx`.

Rename it to `detector_v2_default_checkpoint.onnx.backup`.

Windows:
```
ren detector_v2_default_checkpoint.onnx detector_v2_default_checkpoint.onnx.backup
```
Linux:
```
mv detector_v2_default_checkpoint.onnx detector_v2_default_checkpoint.onnx.backup
```

Convert the checkpoint file:
```
python -m tf2onnx.convert --saved-model <path to extracted archive>\detector_v2_default_checkpoint_tf --opset 11 --output <path to original checkpoint file>\detector_v2_default_checkpoint.onnx
```

This should only take a couple of minutes, (depending on your hardware).
