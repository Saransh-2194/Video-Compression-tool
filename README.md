# Video Compression Tool

This repository contains a small video compression and playback demo with a Streamlit front-end.
The app lets you upload a video, apply simple compression strategies (frame skipping and/or resolution reduction),
optionally re-encode to an H.264/AAC MP4 for browser compatibility, and then play or download the result.

This README explains the project structure, how the tools work, setup and run instructions, and troubleshooting tips.

---

## Project Structure

- `app.py` – Streamlit application. Uploads video files, calls the compressor, shows compressed file properties, and plays the compressed video using Streamlit's built-in video player.
- `video_compression.py` – Contains `VideoProcessor` class with compression methods and helpers:
  - `compress_with_frame_skip(output_path, skip_rate)` — drops frames to reduce FPS/size.
  - `compress_with_resolution(output_path, scale_percent)` — scales frames to reduce resolution.
  - `compress_combined(output_path, skip_rate, scale_percent)` — applies both methods.
  - `compress_to(output_path, method, ...)` — convenience wrapper selecting a method.
  - `compress_video_file(...)` — higher-level helper (used earlier versions).
  - `reencode_to_h264(input_path, output_path)` — (optional) re-encodes with H.264/AAC using MoviePy/ffmpeg for better browser compatibility.
- `video_playback.py` – A local OpenCV-based player/tool (not required by the Streamlit UI). Also contains `get_video_metadata(video_path)`.
- `output/` – Output folder where compressed videos and uploads are saved; `output/uploads/` contains uploaded files.

Other example files (e.g. experiments) may exist in the repo root — the Streamlit app is inside the `Project/` folder.

---

## Requirements

- Python 3.8+
- pip packages (install below)
- ffmpeg (required for reliable H.264 re-encoding and for MoviePy)

Recommended Python packages:

```
pip install streamlit opencv-python numpy moviepy imageio[ffmpeg] matplotlib
```

Notes on ffmpeg:
- On Windows you can install using Chocolatey: `choco install ffmpeg -y` or download a build from https://ffmpeg.org/download.html and add `ffmpeg` to your PATH.
- MoviePy relies on ffmpeg to encode/decode — without it the H.264 re-encode will fail.

---

## Run the Streamlit App (Windows PowerShell example)

1. Open PowerShell and change to the `Project` directory:

```powershell
cd "\Project"
```

2. Launch the app:

```powershell
streamlit run app.py
```

3. In the browser UI:
- Upload a video (`.mp4`, `.avi`, `.mov`). The file will be saved to `output/uploads/`.
- Use the sidebar to choose a compression method:
  - `combined` (frame skip + resolution reduction)
  - `frameskip` (skip frames)
  - `resolution` (scale frames)
- Press `Compress`. A spinner will show while compression runs.
- The compressed file is saved in `output/` and its properties are displayed. The compressed file is playable in the page and available for download.

---


## Troubleshooting & Tips

- If compression fails or is very slow, try smaller inputs or increase `skip_rate` / reduce `scale_percent`.
- If Streamlit shows no video despite a valid file, open that file directly in VLC or Chrome — if VLC plays it but Chrome does not, re-encode to H.264/AAC.
- For production or larger workloads, consider running compression in a background worker and streaming progress to Streamlit (using `st.session_state` or polling).


---
Author: Saransh Agarwal & Nandini Garg
Date: 22 November 2025
