import cv2 as cv
import numpy as np
import moviepy as mp
import tkinter as tk
from pathlib import Path
import matplotlib.pyplot as plt

class VideoProcessor:
    def __init__(self):
        self.cap = None
        self.video_path = None
        self.video_properties = {}

    def load_video(self, video_path):
        """Load video and extract properties"""
        try:
            self.video_path = video_path
            self.cap = cv.VideoCapture(video_path)

            if not self.cap.isOpened():
                raise ValueError("Could not open video file")

            self.video_properties = {
                'fps': self.cap.get(cv.CAP_PROP_FPS),
                'frame_count': int(self.cap.get(cv.CAP_PROP_FRAME_COUNT)),
                'width': int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH)),
                'height': int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)),
                'duration': self.cap.get(cv.CAP_PROP_FRAME_COUNT) / self.cap.get(cv.CAP_PROP_FPS)
            }

            # print("✓ Video loaded successfully!")
            # self.display_properties()
            return True
        except Exception as e:
            # print(f"✗ Error loading video: {e}")
            return False

    def display_properties(self):
        """Display video properties in a readable format"""
        if not self.video_properties:
            print("✗ No video properties available. Load a video first.")
            return

        print("\n" + "="*50)
        print("VIDEO PROPERTIES")
        print("="*50)
        print(f"Resolution: {self.video_properties['width']}x{self.video_properties['height']}")
        print(f"FPS: {self.video_properties['fps']:.2f}")
        print(f"Total Frames: {self.video_properties['frame_count']}")
        print(f"Duration: {self.video_properties['duration']:.2f} seconds")
        print(f"File: {Path(self.video_path).name if self.video_path else 'N/A'}")
        print("="*50 + "\n")

    def show_first_frame(self):
        """Display the first frame of the video using matplotlib"""
        if self.cap is None or not self.cap.isOpened():
            print("✗ No video loaded or video cannot be opened.")
            return

        self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret, frame = self.cap.read()

        if ret:
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            display_frame = self.resize_for_display(frame_rgb)

            plt.figure(figsize=(10, 7))
            plt.imshow(display_frame)
            plt.title("First Frame of the Video")
            plt.axis('off')
            plt.show()
            print("First frame displayed successfully.")
        else:
            print("✗ Could not read first frame.")

    def resize_for_display(self, frame, max_width=1280):
        """Resize frame for display if it's too large"""
        height, width = frame.shape[:2]
        if width > max_width:
            scale = max_width / width
            new_width = max_width
            new_height = int(height * scale)
            return cv.resize(frame, (new_width, new_height))
        return frame

    def _get_video_writer(self, output_path, fps, width, height):
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out = cv.VideoWriter(output_path, fourcc, fps, (width, height))
        if not out.isOpened():
            raise IOError(f"Could not open video writer for {output_path}")
        return out

    def compress_with_frame_skip(self, output_path, skip_rate=2):
        """Compress video by skipping frames"""
        if self.cap is None or not self.cap.isOpened():
            print("✗ No video loaded or video cannot be opened.")
            return False

        if skip_rate < 1:
            print("✗ Skip rate must be at least 1.")
            return False

        print(f"Starting frame skip compression (skip every {skip_rate} frames) to {output_path}...")

        new_fps = self.video_properties['fps'] / skip_rate
        width = self.video_properties['width']
        height = self.video_properties['height']

        out = self._get_video_writer(output_path, new_fps, width, height)
        self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        frame_idx = 0
        processed_frames = 0

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                if frame_idx % skip_rate == 0:
                    out.write(frame)
                    processed_frames += 1
                frame_idx += 1
            print(f"✓ Frame skip compression complete. Wrote {processed_frames} frames.")
            return True
        except Exception as e:
            print(f"✗ Error during frame skip compression: {e}")
            return False
        finally:
            out.release()

    def compress_with_resolution(self, output_path, scale_percent=50):
        """Compress video by reducing resolution"""
        if self.cap is None or not self.cap.isOpened():
            print("✗ No video loaded or video cannot be opened.")
            return False

        if not (1 < scale_percent <= 100):
            print("✗ Scale percent must be between 1 and 100.")
            return False

        print(f"Starting resolution compression ({scale_percent}% scale) to {output_path}...")

        new_width = int(self.video_properties['width'] * scale_percent / 100)
        new_height = int(self.video_properties['height'] * scale_percent / 100)

        fps = self.video_properties['fps']

        out = self._get_video_writer(output_path, fps, new_width, new_height)
        self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        processed_frames = 0

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                resized_frame = cv.resize(frame, (new_width, new_height), interpolation=cv.INTER_AREA)
                out.write(resized_frame)
                processed_frames += 1
            print(f"✓ Resolution compression complete. Wrote {processed_frames} frames.")
            return True
        except Exception as e:
            print(f"✗ Error during resolution compression: {e}")
            return False
        finally:
            out.release()

    def compress_combined(self, output_path, skip_rate=2, scale_percent=50):
        """Compress video using both frame skipping and resolution reduction"""
        if self.cap is None or not self.cap.isOpened():
            print("✗ No video loaded or video cannot be opened.")
            return False

        if skip_rate < 1 or not (1 < scale_percent <= 100):
            print("✗ Invalid skip rate or scale percent.")
            return False

        print(f"Starting combined compression (skip every {skip_rate} frames, {scale_percent}% scale) to {output_path}...")

        new_width = int(self.video_properties['width'] * scale_percent / 100)
        new_height = int(self.video_properties['height'] * scale_percent / 100)
        new_fps = self.video_properties['fps'] / skip_rate

        out = self._get_video_writer(output_path, new_fps, new_width, new_height)
        self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        frame_idx = 0
        processed_frames = 0

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                if frame_idx % skip_rate == 0:
                    resized_frame = cv.resize(frame, (new_width, new_height), interpolation=cv.INTER_AREA)
                    out.write(resized_frame)
                    processed_frames += 1
                frame_idx += 1
            print(f"✓ Combined compression complete. Wrote {processed_frames} frames.")
            return True
        except Exception as e:
            print(f"✗ Error during combined compression: {e}")
            return False
        finally:
            out.release()

    def close(self):
        """Release video capture"""
        if self.cap is not None:
            self.cap.release()
            print("Video capture released.")

    def compress_to(self, output_path, method='combined', skip_rate=2, scale_percent=50):
        """Convenience wrapper to compress loaded video to output_path using chosen method.
        Returns True on success, False otherwise.
        """
        if self.cap is None or not self.cap.isOpened():
            print("✗ No video loaded or video cannot be opened.")
            return False

        if method == 'frameskip':
            return self.compress_with_frame_skip(output_path, skip_rate=skip_rate)
        elif method == 'resolution':
            return self.compress_with_resolution(output_path, scale_percent=scale_percent)
        elif method == 'combined':
            return self.compress_combined(output_path, skip_rate=skip_rate, scale_percent=scale_percent)
        else:
            print(f"✗ Unknown compression method: {method}")
            return False


def compress_video_file(input_path, output_dir, method='combined', skip_rate=2, scale_percent=50):
    """High level helper: load input_path, compress to output_dir, return output_path and metadata dict.
    Metadata includes: path, filesize (bytes), fps, frame_count, width, height, duration
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    name = src.stem + f"_{method}.mp4"
    out_path = str(output_dir / name)

    proc = VideoProcessor()
    try:
        ok = proc.load_video(str(src))
        if not ok:
            raise RuntimeError("Failed to load input video")

        ok = proc.compress_to(out_path, method=method, skip_rate=skip_rate, scale_percent=scale_percent)
        if not ok:
            raise RuntimeError("Compression failed")
    finally:
        proc.close()

    # gather metadata from compressed file
    cap = cv.VideoCapture(out_path)
    if not cap.isOpened():
        raise RuntimeError("Could not open compressed output to read metadata")

    fps = cap.get(cv.CAP_PROP_FPS)
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    cap.release()

    filesize = (Path(out_path).stat().st_size)

    metadata = {
        'path': out_path,
        'filesize': filesize,
        'fps': fps,
        'frame_count': frame_count,
        'width': width,
        'height': height,
        'duration': duration,
    }

    return out_path, metadata


# if __name__ == "__main__":
#     print("Video Compression Tool - Step 1: Basic Video Loading")
#     print("-" * 50)
#     processor = VideoProcessor()


#     video_file = "input.mp4"

#     print(f"Attempting to load: {video_file}")

#     if processor.load_video(video_file):
#         processor.show_first_frame()

#     processor.close()

#     print("\n✓ Step 1 Complete!")
#     print("\nNext: We'll add compression functions (frame skipping & resolution reduction)")

#     processor = VideoProcessor()

# if processor.load_video(video_file):
#     print("\nChoose compression method:")
#     print("1. Frame skip only (skip every 2nd frame)")
#     print("2. Resolution only (50% scale)")
#     print("3. Combined (both methods)")

#     choice = input("\nEnter choice (1-3): ")

#     if choice == "1":
#         processor.compress_with_frame_skip("output_frameskip.mp4", skip_rate=2)
#     elif choice == "2":
#         processor.compress_with_resolution("output_resolution.mp4", scale_percent=50)
#     elif choice == "3":
#         processor.compress_combined("output_combined.mp4", skip_rate=2, scale_percent=50)
#     else:
#         print("Invalid choice")

# processor.close()

