"""
Smart City Surveillance System - Core Detection Module
Provides object detection and tracking capabilities for surveillance.
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict


class ObjectDetector:
    """Simple object detector using OpenCV background subtraction and contour detection."""
    
    def __init__(self, min_contour_area: int = 500):
        """
        Initialize the object detector.
        
        Args:
            min_contour_area: Minimum contour area to be considered as an object
        """
        self.min_contour_area = min_contour_area
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=16, detectShadows=True
        )
        
    def detect_objects(self, frame: np.ndarray) -> Tuple[List[Tuple[int, int, int, int]], np.ndarray]:
        """
        Detect objects in a frame using background subtraction.
        
        Args:
            frame: Input frame as numpy array
            
        Returns:
            Tuple of (list of bounding boxes, processed frame)
            Each bounding box is (x, y, w, h)
        """
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(frame)
        
        # Remove shadows
        fg_mask[fg_mask == 127] = 0
        
        # Apply morphological operations to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Extract bounding boxes
        bboxes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                bboxes.append((x, y, w, h))
        
        return bboxes, fg_mask


class SurveillanceAnalyzer:
    """Analyzes surveillance data and provides statistics."""
    
    def __init__(self):
        """Initialize the surveillance analyzer."""
        self.detection_history = []
        self.max_history = 100
        
    def update(self, num_objects: int):
        """
        Update detection history with new count.
        
        Args:
            num_objects: Number of objects detected in current frame
        """
        self.detection_history.append(num_objects)
        if len(self.detection_history) > self.max_history:
            self.detection_history.pop(0)
    
    def get_statistics(self) -> Dict[str, float]:
        """
        Get statistics from detection history.
        
        Returns:
            Dictionary with statistics (current, average, max)
        """
        if not self.detection_history:
            return {
                'current': 0,
                'average': 0.0,
                'max': 0,
                'min': 0
            }
        
        return {
            'current': self.detection_history[-1],
            'average': np.mean(self.detection_history),
            'max': max(self.detection_history),
            'min': min(self.detection_history)
        }
    
    def get_history(self) -> List[int]:
        """Get detection history."""
        return self.detection_history.copy()


def draw_detections(frame: np.ndarray, bboxes: List[Tuple[int, int, int, int]], 
                    color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
    """
    Draw bounding boxes on frame.
    
    Args:
        frame: Input frame
        bboxes: List of bounding boxes (x, y, w, h)
        color: Color for bounding boxes in BGR format
        
    Returns:
        Frame with drawn bounding boxes
    """
    output = frame.copy()
    for i, (x, y, w, h) in enumerate(bboxes):
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
        cv2.putText(output, f"Object {i+1}", (x, y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    # Add object count
    cv2.putText(output, f"Detected: {len(bboxes)} objects", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return output
