import cv2
import numpy as np
import os

class H261MotionCompensation:
    def __init__(self, block_size=16):
        self.block_size = block_size

    def motion_compensation(self, reference_frame, motion_vectors):
        height, width = reference_frame.shape
        num_blocks_y, num_blocks_x, _ = motion_vectors.shape
        compensated_frame = np.zeros_like(reference_frame)

        for y in range(0, num_blocks_y * self.block_size, self.block_size):
            for x in range(0, num_blocks_x * self.block_size, self.block_size):
                dy, dx = motion_vectors[y // self.block_size, x // self.block_size]
                ref_x = x + dx
                ref_y = y + dy

                if (0 <= ref_x < width - self.block_size + 1 and
                    0 <= ref_y < height - self.block_size + 1):
                    compensated_frame[y:y + self.block_size, x:x + self.block_size] = \
                        reference_frame[ref_y:ref_y + self.block_size, ref_x:ref_x + self.block_size]

        return compensated_frame


def process_motion_compensation(input_path, motion_vectors_file, output_motion_compensation, block_size=16):
    decoder = H261MotionCompensation(block_size=block_size)
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    # Load motion vectors
    motion_vectors_list = np.load(motion_vectors_file, allow_pickle=True)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = len(motion_vectors_list)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_motion_compensation = cv2.VideoWriter(output_motion_compensation, fourcc, fps,
                                              (frame_width, frame_height), isColor=False)

    prev_frame = None
    print(f"Processing {frame_count} frames for motion compensation...")

    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is None:
            out_motion_compensation.write(gray_frame)
        else:
            motion_vectors = motion_vectors_list[i - 1]
            compensated_frame = decoder.motion_compensation(prev_frame, motion_vectors)
            out_motion_compensation.write(compensated_frame)

        prev_frame = gray_frame
        if i % 10 == 0:
            print(f"Processed {i}/{frame_count} frames...")

    cap.release()
    out_motion_compensation.release()
    print(f"Motion Compensation complete! Output video: {output_motion_compensation}")


if __name__ == "__main__":
    input_path = input("Enter the path to the input AVI video file: ").strip()
    motion_vectors_file = "motion_vectors.npy"
    output_motion_compensation = "motion_compensation.mp4"

    if not os.path.exists(input_path) or not os.path.exists(motion_vectors_file):
        print("Error: Input file or motion vectors file does not exist.")
        exit(1)

    process_motion_compensation(input_path, motion_vectors_file, output_motion_compensation)
