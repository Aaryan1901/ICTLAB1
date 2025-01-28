import cv2
import numpy as np
import os

class H261MotionEstimation:
    def __init__(self, block_size=16, search_range=8):
        self.block_size = block_size
        self.search_range = search_range

    def motion_estimation(self, current_frame, reference_frame):
        height, width = current_frame.shape
        num_blocks_y = height // self.block_size
        num_blocks_x = width // self.block_size
        motion_vectors = np.zeros((num_blocks_y, num_blocks_x, 2), dtype=int)

        for y in range(0, num_blocks_y * self.block_size, self.block_size):
            for x in range(0, num_blocks_x * self.block_size, self.block_size):
                best_match = (0, 0)
                min_error = float('inf')
                current_block = current_frame[y:y + self.block_size, x:x + self.block_size]

                for dy in range(-self.search_range, self.search_range + 1):
                    for dx in range(-self.search_range, self.search_range + 1):
                        ref_x = x + dx
                        ref_y = y + dy
                        if (0 <= ref_x < width - self.block_size + 1 and
                            0 <= ref_y < height - self.block_size + 1):
                            ref_block = reference_frame[ref_y:ref_y + self.block_size,
                                                        ref_x:ref_x + self.block_size]
                            error = np.sum((current_block - ref_block) ** 2)
                            if error < min_error:
                                min_error = error
                                best_match = (dy, dx)

                motion_vectors[y // self.block_size, x // self.block_size] = best_match

        return motion_vectors

    def draw_motion_vectors(self, frame, motion_vectors):
        frame_with_vectors = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        for y in range(motion_vectors.shape[0]):
            for x in range(motion_vectors.shape[1]):
                dy, dx = motion_vectors[y, x]
                start_point = (x * self.block_size + self.block_size // 2,
                               y * self.block_size + self.block_size // 2)
                end_point = (start_point[0] + dx, start_point[1] + dy)
                cv2.arrowedLine(frame_with_vectors, start_point, end_point,
                                (0, 0, 255), 1, tipLength=0.4)

        return frame_with_vectors


def process_motion_estimation(input_path, output_motion_estimation, motion_vectors_file,
                              block_size=16, search_range=8):
    encoder = H261MotionEstimation(block_size=block_size, search_range=search_range)
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_motion_estimation = cv2.VideoWriter(output_motion_estimation, fourcc, fps,
                                            (frame_width, frame_height))

    prev_frame = None
    motion_vectors_list = []
    print(f"Processing {frame_count} frames for motion estimation...")

    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is None:
            out_motion_estimation.write(cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR))
        else:
            motion_vectors = encoder.motion_estimation(gray_frame, prev_frame)
            motion_estimation_frame = encoder.draw_motion_vectors(prev_frame, motion_vectors)
            motion_vectors_list.append(motion_vectors)
            out_motion_estimation.write(motion_estimation_frame)

        prev_frame = gray_frame
        if i % 10 == 0:
            print(f"Processed {i}/{frame_count} frames...")

    cap.release()
    out_motion_estimation.release()

    # Save motion vectors to .npy file
    np.save(motion_vectors_file, np.array(motion_vectors_list))
    print(f"Motion Estimation complete! Outputs:")
    print(f" - Motion Estimation video: {output_motion_estimation}")
    print(f" - Motion Vectors file: {motion_vectors_file}")


if __name__ == "__main__":
    input_path = input("Enter the path to the input AVI video file: ").strip()
    output_motion_estimation = "motion_estimation.mp4"
    motion_vectors_file = "motion_vectors.npy"

    if not os.path.exists(input_path):
        print("Error: Input file does not exist.")
        exit(1)

    process_motion_estimation(input_path, output_motion_estimation, motion_vectors_file)
