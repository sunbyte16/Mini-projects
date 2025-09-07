#!/usr/bin/env python3
"""
Test script for AI Hand Detection System
This script tests all major components of the system
"""

import sys
import os
import time
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import mediapipe as mp
        print("✓ MediaPipe imported successfully")
    except ImportError as e:
        print(f"✗ MediaPipe import failed: {e}")
        return False
    
    try:
        from flask import Flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    return True

def test_hand_detection_module():
    """Test the hand detection module"""
    print("\nTesting hand detection module...")
    
    try:
        from hand_detection import HandDetector
        print("✓ HandDetector class imported successfully")
        
        # Test initialization
        detector = HandDetector()
        print("✓ HandDetector initialized successfully")
        
        # Test with a dummy image
        import numpy as np
        dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Test find_hands method
        result_img = detector.find_hands(dummy_img)
        print("✓ find_hands method works")
        
        # Test detect_gesture method
        gesture, result_img = detector.detect_gesture(dummy_img)
        print("✓ detect_gesture method works")
        
        # Test get_hand_landmarks method
        landmarks = detector.get_hand_landmarks(dummy_img)
        print("✓ get_hand_landmarks method works")
        
        # Clean up
        detector.hands.close()
        print("✓ HandDetector cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Hand detection module test failed: {e}")
        traceback.print_exc()
        return False

def test_camera_access():
    """Test camera access"""
    print("\nTesting camera access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Camera not accessible")
            return False
        
        # Try to read a frame
        ret, frame = cap.read()
        if not ret:
            print("✗ Cannot read from camera")
            cap.release()
            return False
        
        print("✓ Camera access successful")
        cap.release()
        return True
        
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_flask_app():
    """Test Flask app functionality"""
    print("\nTesting Flask app...")
    
    try:
        from app import app
        
        # Test if app can be created
        with app.test_client() as client:
            # Test main route
            response = client.get('/')
            if response.status_code == 200:
                print("✓ Main route works")
            else:
                print("✗ Main route failed")
                return False
            
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print("✓ Health endpoint works")
            else:
                print("✗ Health endpoint failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        traceback.print_exc()
        return False

def test_dependencies():
    """Test if all dependencies are installed"""
    print("\nTesting dependencies...")
    
    required_packages = [
        'flask',
        'flask-cors',
        'opencv-python',
        'numpy',
        'mediapipe'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'flask-cors':
                import flask_cors
            else:
                __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🤖 AI Hand Detection System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Hand Detection Module", test_hand_detection_module),
        ("Camera Access", test_camera_access),
        ("Flask App", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nTo run the system:")
        print("  Desktop: python hand_detection.py")
        print("  Web:      python app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Ensure camera is connected and not in use")
        print("  3. Check if all files are in the correct directory")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 