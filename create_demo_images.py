"""
Demo script to generate sample images for testing the surveillance system.
This creates simple test images with moving objects.
"""

import numpy as np
import cv2
import os


def create_sample_images():
    """Create sample images for testing the surveillance system."""
    
    # Create output directory
    output_dir = "/tmp/demo_images"
    os.makedirs(output_dir, exist_ok=True)
    
    # Image dimensions
    height, width = 480, 640
    
    # 1. Create a static background image
    background = np.ones((height, width, 3), dtype=np.uint8) * 50
    # Add some texture
    for i in range(0, height, 20):
        cv2.line(background, (0, i), (width, i), (60, 60, 60), 1)
    for i in range(0, width, 20):
        cv2.line(background, (i, 0), (i, height), (60, 60, 60), 1)
    
    cv2.imwrite(f"{output_dir}/background.jpg", background)
    print(f"Created: {output_dir}/background.jpg")
    
    # 2. Create image with one object
    img1 = background.copy()
    cv2.rectangle(img1, (200, 150), (350, 300), (255, 100, 100), -1)
    cv2.putText(img1, "Car", (220, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite(f"{output_dir}/one_object.jpg", img1)
    print(f"Created: {output_dir}/one_object.jpg")
    
    # 3. Create image with multiple objects
    img2 = background.copy()
    # Object 1 - Vehicle
    cv2.rectangle(img2, (100, 200), (200, 280), (100, 150, 255), -1)
    cv2.putText(img2, "V1", (130, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Object 2 - Person
    cv2.circle(img2, (350, 220), 30, (150, 255, 150), -1)
    cv2.putText(img2, "P1", (335, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Object 3 - Vehicle
    cv2.rectangle(img2, (450, 100), (580, 180), (255, 200, 100), -1)
    cv2.putText(img2, "V2", (490, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    cv2.imwrite(f"{output_dir}/multiple_objects.jpg", img2)
    print(f"Created: {output_dir}/multiple_objects.jpg")
    
    # 4. Create a sequence of frames for video-like testing
    print("\nCreating frame sequence for video simulation...")
    frames_dir = f"{output_dir}/frames"
    os.makedirs(frames_dir, exist_ok=True)
    
    for i in range(30):
        frame = background.copy()
        # Moving object from left to right
        x_pos = int(50 + i * 18)
        cv2.rectangle(frame, (x_pos, 200), (x_pos + 80, 280), (100, 200, 255), -1)
        cv2.putText(frame, "Moving", (x_pos + 5, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imwrite(f"{frames_dir}/frame_{i:03d}.jpg", frame)
    
    print(f"Created 30 frames in: {frames_dir}/")
    
    print(f"\n✅ Sample images created successfully in: {output_dir}")
    print(f"\nYou can use these images to test the Streamlit application:")
    print(f"  - background.jpg: Static background")
    print(f"  - one_object.jpg: Single object")
    print(f"  - multiple_objects.jpg: Multiple objects")
    print(f"  - frames/: Sequence of frames simulating motion")


if __name__ == "__main__":
    create_sample_images()
