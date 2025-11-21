import cv2
import numpy as np
import moviepy as mp
import tkinter as tk
from pathlib import Path
import matplotlib.pyplot as plt

class VideoPlayer:
    def __init__(self):
        self.cap = None
        self.video_path = None
        self.video_properties = {}
        self.is_playing = True
        self.window_name = "Video Player"
        self.fps = 30
        self.total_frames = 0
        self.duration = 0
        self.current_frame = 0

    def load_video(self, video_path):
        """Load video file and initialize playback state"""
        try:
            self.video_path = video_path
            self.cap = cv2.VideoCapture(video_path)

            if not self.cap.isOpened():
                print("✗ Could not open video file")
                return False

            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
            self.duration = (self.total_frames / self.fps) if self.fps > 0 else 0
            self.current_frame = 0

            print(f"✓ Video loaded! FPS: {self.fps:.2f}")
            return True

        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def format_time(self, seconds):
        """Convert seconds to MM:SS format"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def get_current_time(self):
        """Get current playback time"""
        return self.current_frame / self.fps if self.fps > 0 else 0

    def jump_to_frame(self, frame_number):
        """Jump to a specific frame"""
        frame_number = max(0, min(frame_number, self.total_frames - 1))
        self.current_frame = frame_number
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def next_frame(self):
        """Go to next frame"""
        if self.current_frame < self.total_frames - 1:
            self.jump_to_frame(self.current_frame + 1)
            print(f"→ Frame {self.current_frame}")
        else:
            print("Already at last frame")

    def previous_frame(self):
        """Go to previous frame"""
        if self.current_frame > 0:
            self.jump_to_frame(self.current_frame - 1)
            print(f"← Frame {self.current_frame}")
        else:
            print("Already at first frame")

    def add_info_overlay(self, frame):
        """Add info text overlay on the frame"""
        display_frame = frame.copy()
        height, width = frame.shape[:2]

        overlay = display_frame.copy()
        cv2.rectangle(overlay, (10, height-90), (350, height-10), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, display_frame, 0.3, 0, display_frame)

        status_text = "▶ PLAYING" if self.is_playing else "⏸ PAUSED"
        status_color = (0, 255, 0) if self.is_playing else (0, 165, 255)

        y_position = height - 70
        cv2.putText(display_frame, status_text, (20, y_position),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

        y_position += 25
        frame_text = f"Frame: {self.current_frame} / {self.total_frames}"
        cv2.putText(display_frame, frame_text, (20, y_position),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        y_position += 25
        time_text = f"Time: {self.format_time(self.get_current_time())} / {self.format_time(self.duration)}"
        cv2.putText(display_frame, time_text, (20, y_position),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return display_frame

    def play(self):
        """Main playback loop"""
        if self.cap is None:
            print("✗ No video loaded")
            return

        print("\n" + "="*40)
        print("CONTROLS")
        print("="*40)
        print("SPACE       : Play/Pause")
        print("→ (Right)   : Next frame")
        print("← (Left)    : Previous frame")
        print("Q           : Quit")
        print("="*40 + "\n")

        frame_delay = int(1000 / self.fps) if self.fps > 0 else 33

        while True:
            if self.is_playing:
                ret, frame = self.cap.read()

                if not ret:
                    print("Video ended - returning to start")
                    self.is_playing = False
                    self.jump_to_frame(0)
                    continue

                self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

            else:
                # when paused, ensure we read the current frame
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
                ret, frame = self.cap.read()
                if not ret:
                    break

            display_frame = self.add_info_overlay(frame)

            cv2.imshow(self.window_name, display_frame)

            key = cv2.waitKey(frame_delay if self.is_playing else 30) & 0xFF

            if key == ord('q') or key == 27:
                print("👋 Quitting")
                break

            elif key == ord(' '):
                self.is_playing = not self.is_playing
                status = "Playing" if self.is_playing else "Paused"
                print(f"{ '▶' if self.is_playing else '⏸' } {status}")

            elif key == 83:  # right arrow
                self.is_playing = False
                self.next_frame()

            elif key == 81:  # left arrow
                self.is_playing = False
                self.previous_frame()

        self.cap.release()
        cv2.destroyAllWindows()


def load_video(self, video_path):
    """Load video file"""
    try:
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            print("✗ Could not open video file")
            return False

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.total_frames / self.fps

        print(f"✓ Video loaded!")
        print(f"  FPS: {self.fps:.2f}")
        print(f"  Total Frames: {self.total_frames}")
        print(f"  Duration: {self.format_time(self.duration)}")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def format_time(self, seconds):
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def get_current_time(self):
    """Get current playback time"""
    return self.current_frame / self.fps

def jump_to_frame(self, frame_number):
    """Jump to a specific frame"""
    frame_number = max(0, min(frame_number, self.total_frames - 1))
    self.current_frame = frame_number
    self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

def next_frame(self):
    """Go to next frame"""
    if self.current_frame < self.total_frames - 1:
        self.jump_to_frame(self.current_frame + 1)
        print(f"→ Frame {self.current_frame}")
    else:
        print("Already at last frame")

def previous_frame(self):
    """Go to previous frame"""
    if self.current_frame > 0:
        self.jump_to_frame(self.current_frame - 1)
        print(f"← Frame {self.current_frame}")
    else:
        print("Already at first frame")

def add_info_overlay(self, frame):
    """Add info text overlay on the frame"""
    display_frame = frame.copy()
    height, width = frame.shape[:2]

    overlay = display_frame.copy()
    cv2.rectangle(overlay, (10, height-90), (350, height-10), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, display_frame, 0.3, 0, display_frame)

    status_text = "▶ PLAYING" if self.is_playing else "⏸ PAUSED"
    status_color = (0, 255, 0) if self.is_playing else (0, 165, 255)

    y_position = height - 70
    cv2.putText(display_frame, status_text, (20, y_position),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

    y_position += 25
    frame_text = f"Frame: {self.current_frame} / {self.total_frames}"
    cv2.putText(display_frame, frame_text, (20, y_position),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    y_position += 25
    time_text = f"Time: {self.format_time(self.get_current_time())} / {self.format_time(self.duration)}"
    cv2.putText(display_frame, time_text, (20, y_position),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return display_frame

def play(self):
    """Main playback loop"""
    if self.cap is None:
        print("✗ No video loaded")
        return

    print("\n" + "="*40)
    print("CONTROLS")
    print("="*40)
    print("SPACE       : Play/Pause")
    print("→ (Right)   : Next frame")
    print("← (Left)    : Previous frame")
    print("Q           : Quit")
    print("="*40 + "\n")

    frame_delay = int(1000 / self.fps)

    while True:
        if self.is_playing:
            ret, frame = self.cap.read()

            if not ret:
                print("Video ended - returning to start")
                self.is_playing = False
                self.jump_to_frame(0)
                continue

            self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            ret, frame = self.cap.read()

            if not ret:
                break

        display_frame = self.add_info_overlay(frame)

        cv2.imshow(self.window_name, display_frame)

        key = cv2.waitKey(frame_delay if self.is_playing else 30) & 0xFF

        if key == ord('q') or key == 27:
            print("👋 Quitting")
            break

        elif key == ord(' '):
            self.is_playing = not self.is_playing
            status = "Playing" if self.is_playing else "Paused"
            print(f"{'▶' if self.is_playing else '⏸'} {status}")

        elif key == 83:
            self.is_playing = False
            self.next_frame()

        elif key == 81:
            self.is_playing = False
            self.previous_frame()

    self.cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     print("Video Player - Step 3B: Frame Info Display")
#     print("-" * 40)
#     player = VideoPlayer()

# video_file = "input.mp4"

# if player.load_video(video_file):
#     player.play()


def get_video_metadata(video_path):
    """Return basic metadata for the given video file as a dict.
    Keys: fps, frame_count, width, height, duration, filesize
    """
    p = Path(video_path)
    if not p.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError("Could not open video file to read metadata")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    cap.release()

    return {
        'fps': fps,
        'frame_count': frame_count,
        'width': width,
        'height': height,
        'duration': duration,
        'filesize': p.stat().st_size,
        'path': str(p)
    }

