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
cd "c:\Users\saran\OneDrive\Desktop\JUIT\sem files\sem-5\Multimedia Lab\Project"
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
- Optional: use the H.264 re-encode option (if available) to produce a browser-friendly MP4.
- Press `Compress`. A spinner will show while compression (and optional re-encode) runs.
- The compressed file is saved in `output/` and its properties are displayed. The compressed file is playable in the page and available for download.

---

## Why the video might show a black player / 0:00

If the Streamlit player shows a black box or `0:00` the browser probably cannot decode the codec/container in the file. Common causes:

- The output MP4 uses a codec not supported by browser players (browsers expect H.264 video + AAC audio in MP4).
- ffmpeg or MoviePy is not installed/configured, so the optional re-encode step did not produce a browser-compatible file.

Fixes:

- Re-encode the compressed file to H.264/AAC (the app provides an option if MoviePy/ffmpeg are available).
- Or re-encode manually using ffmpeg:

```powershell
ffmpeg -i "path\to\input.mp4" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k "path\to\output_h264.mp4"
```

Then try playing `output_h264.mp4` in the app or directly in the browser/VLC.

---

## Internals / Implementation notes

- Compression uses OpenCV's `VideoWriter` with `mp4v` fourcc by default. `mp4v` may not always be browser-friendly.
- `reencode_to_h264` uses MoviePy (`write_videofile`) with `codec='libx264'` and `audio_codec='aac'` to produce a more compatible MP4. MoviePy must find ffmpeg on PATH.
- `app.py` verifies that compressed files exist and attempts a quick sanity check (OpenCV read) before calling `st.video`.

---

## Troubleshooting & Tips

- If compression fails or is very slow, try smaller inputs or increase `skip_rate` / reduce `scale_percent`.
- If re-encoding fails, install ffmpeg and ensure it's in PATH. Test with `ffmpeg -version`.
- If Streamlit shows no video despite a valid file, open that file directly in VLC or Chrome — if VLC plays it but Chrome does not, re-encode to H.264/AAC.
- For production or larger workloads, consider running compression in a background worker and streaming progress to Streamlit (using `st.session_state` or polling).

---

## Next improvements (suggestions)

- Use ffprobe to display more detailed codec/bitrate metadata.
- Add background processing + progress updates for long compressions.
- Provide configurable ffmpeg re-encoding parameters (CRF, preset, audio bitrate).
- Add unit tests and a `requirements.txt`/`pyproject.toml` file for reproducible installs.

---

If you want, I can add a `requirements.txt` and a simple test script, or implement the ffmpeg CLI fallback re-encode (recommended for robustness). Which would you like next?

---
Author: Project workspace (Video-Compression-tool)
Date: November 2025
