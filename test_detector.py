"""
Test suite for Smart City Surveillance System
"""

import unittest
import numpy as np
import cv2
from detector import ObjectDetector, SurveillanceAnalyzer, draw_detections


class TestObjectDetector(unittest.TestCase):
    """Test cases for ObjectDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = ObjectDetector(min_contour_area=500)
    
    def test_detector_initialization(self):
        """Test detector initializes correctly."""
        self.assertIsNotNone(self.detector)
        self.assertEqual(self.detector.min_contour_area, 500)
    
    def test_detect_objects_empty_frame(self):
        """Test detection on empty frame."""
        # Create a blank frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        bboxes, fg_mask = self.detector.detect_objects(frame)
        
        # Should return empty list initially
        self.assertIsInstance(bboxes, list)
        self.assertIsNotNone(fg_mask)
    
    def test_detect_objects_with_motion(self):
        """Test detection with simulated motion."""
        # Create detector and send multiple frames to initialize background
        detector = ObjectDetector(min_contour_area=100)
        
        # Initialize with static background
        for _ in range(10):
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            detector.detect_objects(frame)
        
        # Add a white rectangle (simulating moving object)
        frame_with_object = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(frame_with_object, (200, 200), (400, 400), (255, 255, 255), -1)
        
        bboxes, _ = detector.detect_objects(frame_with_object)
        
        # Should detect something
        self.assertIsInstance(bboxes, list)


class TestSurveillanceAnalyzer(unittest.TestCase):
    """Test cases for SurveillanceAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SurveillanceAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly."""
        self.assertIsNotNone(self.analyzer)
        self.assertEqual(len(self.analyzer.detection_history), 0)
    
    def test_update(self):
        """Test update method."""
        self.analyzer.update(5)
        self.assertEqual(len(self.analyzer.detection_history), 1)
        self.assertEqual(self.analyzer.detection_history[0], 5)
    
    def test_get_statistics_empty(self):
        """Test statistics with empty history."""
        stats = self.analyzer.get_statistics()
        
        self.assertEqual(stats['current'], 0)
        self.assertEqual(stats['average'], 0.0)
        self.assertEqual(stats['max'], 0)
        self.assertEqual(stats['min'], 0)
    
    def test_get_statistics_with_data(self):
        """Test statistics with data."""
        values = [1, 2, 3, 4, 5]
        for val in values:
            self.analyzer.update(val)
        
        stats = self.analyzer.get_statistics()
        
        self.assertEqual(stats['current'], 5)
        self.assertEqual(stats['average'], 3.0)
        self.assertEqual(stats['max'], 5)
        self.assertEqual(stats['min'], 1)
    
    def test_history_max_limit(self):
        """Test that history doesn't exceed max limit."""
        for i in range(150):
            self.analyzer.update(i)
        
        self.assertEqual(len(self.analyzer.detection_history), 100)
    
    def test_get_history(self):
        """Test get_history returns a copy."""
        self.analyzer.update(10)
        history = self.analyzer.get_history()
        
        # Modify the returned history
        history.append(999)
        
        # Original should be unchanged
        self.assertEqual(len(self.analyzer.detection_history), 1)


class TestDrawDetections(unittest.TestCase):
    """Test cases for draw_detections function."""
    
    def test_draw_detections_empty(self):
        """Test drawing with no detections."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        bboxes = []
        
        result = draw_detections(frame, bboxes)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.shape, frame.shape)
    
    def test_draw_detections_with_boxes(self):
        """Test drawing with bounding boxes."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        bboxes = [(100, 100, 50, 50), (200, 200, 60, 60)]
        
        result = draw_detections(frame, bboxes)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.shape, frame.shape)
        # Frame should be modified (not all zeros)
        self.assertFalse(np.all(result == frame))
    
    def test_draw_detections_custom_color(self):
        """Test drawing with custom color."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        bboxes = [(100, 100, 50, 50)]
        
        result = draw_detections(frame, bboxes, color=(255, 0, 0))
        
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
