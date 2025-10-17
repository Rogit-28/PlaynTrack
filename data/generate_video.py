import numpy as np
import cv2

def generate_synthetic_video(output_path='video.mp4', width=1280, height=720, frames=300, fps=30):
    """
    Generates a synthetic video of a white ball moving across a black background.
    """
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    ball_radius = 20
    # Start position
    x, y = 100, height // 2
    # Movement vector
    vx, vy = 8, 4

    for i in range(frames):
        # Create a black frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Draw a white ball
        cv2.circle(frame, (int(x), int(y)), ball_radius, (255, 255, 255), -1)

        # Write the frame
        out.write(frame)

        # Update ball position
        x += vx
        y += vy

        # Bounce off the walls
        if x + ball_radius > width or x - ball_radius < 0:
            vx = -vx
        if y + ball_radius > height or y - ball_radius < 0:
            vy = -vy

    out.release()
    print(f"Synthetic video saved to {output_path}")

if __name__ == "__main__":
    generate_synthetic_video()