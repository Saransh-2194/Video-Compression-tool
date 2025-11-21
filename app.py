import streamlit as st
from pathlib import Path
import tempfile
import shutil

from video_compression import VideoProcessor
from video_playback import get_video_metadata

st.title("Video Compressor & Player")
st.write("Upload a video, compress it to `output/`, view properties, and play the compressed file.")

# Prepare output directories
ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "output"
UPLOADS_DIR = OUTPUT_DIR / "uploads"
OUTPUT_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if uploaded_file is None:
    st.info("Please upload a video file to get started.")
else:
    # Save uploaded file to uploads dir
    temp_path = UPLOADS_DIR / uploaded_file.name
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Saved upload to: {temp_path}")

    # Show compression options
    st.sidebar.header("Compression Options")
    method = st.sidebar.selectbox("Method", ["combined", "frameskip", "resolution"], index=0)
    skip_rate = st.sidebar.slider("Skip rate (frames)", 1, 10, 2)
    scale_percent = st.sidebar.slider("Scale percent (resolution)", 10, 100, 50)

    # create processor instance to use class methods
    processor = VideoProcessor()

    if st.button("Compress"):
        try:
            # load the saved upload into processor
            ok = processor.load_video(str(temp_path))
            if not ok:
                st.error("Failed to load uploaded video for compression")
            else:
                out_name = f"{temp_path.stem}_{method}.mp4"
                out_path = OUTPUT_DIR / out_name
                # show spinner while compressing
                with st.spinner("Compressing video... this may take a while"):
                    ok = processor.compress_to(str(out_path), method=method, skip_rate=skip_rate, scale_percent=scale_percent)
                processor.close()
                if not ok:
                    st.error("Compression failed")
                else:
                    st.success("Compression finished")
                    # optionally create a browser-compatible copy
                    compat_path = out_path

                    # read metadata using helper
                    meta = get_video_metadata(str(compat_path))

                    # Display properties
                    st.subheader("Compressed video properties")
                    st.write(f"**Path:** {compat_path}")
                    st.write(f"**Filesize:** {meta['filesize'] / (1024*1024):.2f} MB")
                    st.write(f"**Resolution:** {meta['width']} x {meta['height']}")
                    st.write(f"**FPS:** {meta['fps']:.2f}")
                    st.write(f"**Duration:** {meta['duration']:.2f} seconds")
                    out_path_obj = Path(compat_path)

                    # # Playback widget - stream file bytes to Streamlit
                    # st.subheader("Play compressed video")
                    # if out_path_obj.exists() and out_path_obj.stat().st_size > 0:
                    #     with open(out_path_obj, "rb") as vf:
                    #         video_bytes = vf.read()
                    #     st.video(video_bytes)
                    # else:
                    #     st.error("Compressed file not found or is empty; cannot play.")

                    # Download button (serve the compat copy if created)
                    with open(compat_path, "rb") as f:
                        st.download_button("Download compressed video", f, file_name=Path(compat_path).name)
        except Exception as e:
            st.error(f"Compression failed: {e}")
