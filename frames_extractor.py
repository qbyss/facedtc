import argparse
import cv2
import time
import os
from tqdm import tqdm

def parse_time(time_str):
    """
    Parse a time string in the format of "HH:MM:SS" or "MM:SS" into seconds.

    Args:
    time_str (str): The time string to parse.

    Returns:
    float: The time in seconds.
    """
    time_parts = [float(part) for part in time_str.split(":")]
    time_seconds = sum(part * 60 ** i for i, part in enumerate(reversed(time_parts)))
    return time_seconds

def extract_frames(input_file, output_dir, start_time, end_time, interval):
    """
    Extract frames from an MP4 video file at a specified timestamp interval.

    Args:
    input_file (str): Path to the input MP4 file.
    output_dir (str): Path to the output directory where extracted frames will be saved.
    start_time (float): Start time (in seconds) from where to extract frames.
    end_time (float): End time (in seconds) until where to extract frames.
    interval (float): Time interval (in seconds) between each extracted frame.
    """
    cap = cv2.VideoCapture(input_file)
    start_frame = int(start_time * cap.get(cv2.CAP_PROP_FPS))
    end_frame = int(end_time * cap.get(cv2.CAP_PROP_FPS))
    total_frames = (end_frame - start_frame) // int(interval * cap.get(cv2.CAP_PROP_FPS)) + 1
    current_frame = start_frame
    frame_count = 0

    progress_bar = tqdm(total=total_frames, desc="Extracting frames")

    while True:
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            if not ret:
                break
            if current_frame >= start_frame and current_frame <= end_frame and frame_count % int(interval * cap.get(cv2.CAP_PROP_FPS)) == 0:
                output_file = f"{output_dir}/frame_{current_frame}.jpg"
                cv2.imwrite(output_file, frame)
                #print(f"Extracted frame {current_frame}.")
                progress_bar.update(1)
            current_frame += 1
            frame_count += 1
            if current_frame > end_frame:
                break
        except KeyboardInterrupt:
            print("User interrupted the script.")
            break
    cap.release()
    progress_bar.close()
    print(f"Extracted {frame_count} frames.")


# Extract frame in specified directory buut only keeps those that have a face in it
def extract_frames_with_faces(input_file, output_dir, start_time, end_time, interval, minNeighbors=5, faceMinSize=100):
    """
    Extract frames from an MP4 video file at a specified timestamp interval.

    Args:
    input_file (str): Path to the input MP4 file.
    output_dir (str): Path to the output directory where extracted frames will be saved.
    start_time (float): Start time (in seconds) from where to extract frames.
    end_time (float): End time (in seconds) until where to extract frames.
    interval (float): Time interval (in seconds) between each extracted frame.
    minNeighbors (int): Face detection precision
    faceMinSize (int): Face minimum size detection in pixels
    """
    cap = cv2.VideoCapture(input_file)
    start_frame = int(start_time * cap.get(cv2.CAP_PROP_FPS))
    end_frame = int(end_time * cap.get(cv2.CAP_PROP_FPS))
    total_frames = (end_frame - start_frame) // int(interval * cap.get(cv2.CAP_PROP_FPS)) + 1
    current_frame = start_frame
    frame_count = 0
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    progress_bar = tqdm(total=total_frames, desc="Extracting frames")
    
    while True:
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            if not ret:
                break
            if current_frame >= start_frame and current_frame <= end_frame and frame_count % int(interval * cap.get(cv2.CAP_PROP_FPS)) == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=minNeighbors, minSize=(faceMinSize, faceMinSize))
                if len(faces) > 0:
                    output_file = f"{output_dir}/frame_{current_frame}.jpg"
                    cv2.imwrite(output_file, frame)
                    #print(f"Extracted frame {current_frame}.")
                progress_bar.update(1)
            current_frame += 1
            frame_count += 1
            if current_frame > end_frame:
                break
        except KeyboardInterrupt:
            print("User interrupted the script.")
            break
    cap.release()
    progress_bar.close()
    print(f"Extracted {frame_count} frames.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from an MP4 video file at a specified timestamp interval.")
    parser.add_argument("source", type=str, help="Path to the input MP4 file.")
    parser.add_argument("--start", type=str, required=True, help="Start time in the format of HH:MM:SS or MM:SS.")
    parser.add_argument("--stop", type=str, required=True, help="Stop time in the format of HH:MM:SS or MM:SS.")
    parser.add_argument("--interval", type=float, default=1.0, help="Time interval between extracted frames (in seconds)(default=1).")
    parser.add_argument("--face-size", type=int, default=100, help="Minimum face detection size (default=100).")
    parser.add_argument("--detection-quality", type=int, default=5, help="Face detection quality, higher is better quality. (default=5)")
    parser.add_argument("--directory", type=str, default=".", help="Directory where the captures will be placed.")
    parser.add_argument("--face-only", action="store_true", help="Extract only frames with a face.")

    args = parser.parse_args()

    if not os.path.exists(args.directory) and args.directory != '.':
        os.makedirs(args.directory)

    start_time = parse_time(args.start)
    end_time = parse_time(args.stop)
    if args.face_only:
        extract_frames_with_faces(args.source, args.directory, start_time, end_time, args.interval, args.detection_quality, args.face_size)
    else:
        extract_frames(args.source, args.directory, start_time, end_time, args.interval)
