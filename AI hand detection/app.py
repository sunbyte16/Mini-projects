from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
import base64
from hand_detection import HandDetector
import threading
import time
import os

app = Flask(__name__)
CORS(app)

# Global variables for hand detection
detector = None
camera = None
is_running = False
current_frame = None
detection_results = {}

def initialize_detector():
    """Initialize the hand detector"""
    global detector
    try:
        detector = HandDetector()
        return True
    except Exception as e:
        print(f"Error initializing detector: {e}")
        return False

def start_camera():
    """Start camera capture in a separate thread"""
    global camera, is_running, current_frame, detection_results
    
    if not initialize_detector():
        return False
    
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open camera")
        return False
    
    is_running = True
    
    def camera_loop():
        global current_frame, detection_results
        while is_running:
            success, frame = camera.read()
            if success:
                # Flip frame for selfie view
                frame = cv2.flip(frame, 1)
                
                # Process frame for hand detection
                processed_frame, hand_count = detector.find_hands(frame.copy())
                
                # Get landmarks
                landmarks = detector.get_hand_landmarks(frame)
                
                # Update results
                detection_results = {
                    'landmarks': landmarks,
                    'hand_count': hand_count,
                    'timestamp': time.time()
                }
                
                current_frame = processed_frame
            else:
                time.sleep(0.1)
    
    # Start camera thread
    camera_thread = threading.Thread(target=camera_loop, daemon=True)
    camera_thread.start()
    return True

def stop_camera():
    """Stop camera capture"""
    global camera, is_running
    is_running = False
    if camera:
        camera.release()
    if detector and hasattr(detector, 'hands') and detector.hands:
        detector.hands.close()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_detection():
    """Start hand detection"""
    try:
        if start_camera():
            return jsonify({'success': True, 'message': 'Hand detection started'})
        else:
            return jsonify({'success': False, 'message': 'Failed to start camera'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/stop', methods=['POST'])
def stop_detection():
    """Stop hand detection"""
    try:
        stop_camera()
        return jsonify({'success': True, 'message': 'Hand detection stopped'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/status')
def get_status():
    """Get current detection status"""
    try:
        return jsonify({
            'success': True,
            'is_running': is_running,
            'hand_count': detection_results.get('hand_count', 0),
            'timestamp': detection_results.get('timestamp', 0)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/frame')
def get_frame():
    """Get current camera frame"""
    try:
        if current_frame is not None:
            # Encode frame to JPEG
            _, buffer = cv2.imencode('.jpg', current_frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            return jsonify({
                'success': True,
                'frame': frame_data,
                'timestamp': time.time()
            })
        else:
            return jsonify({'success': False, 'message': 'No frame available'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/landmarks')
def get_landmarks():
    """Get current hand landmarks"""
    try:
        return jsonify({
            'success': True,
            'landmarks': detection_results.get('landmarks', []),
            'hand_count': detection_results.get('hand_count', 0)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/screenshot', methods=['POST'])
def save_screenshot():
    """Save current frame as screenshot"""
    try:
        if current_frame is not None:
            # Create screenshots directory if it doesn't exist
            os.makedirs('screenshots', exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f'screenshots/hand_detection_{timestamp}.jpg'
            
            # Save image
            cv2.imwrite(filename, current_frame)
            
            return jsonify({
                'success': True,
                'message': f'Screenshot saved as {filename}',
                'filename': filename
            })
        else:
            return jsonify({'success': False, 'message': 'No frame available'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'camera_running': is_running
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting AI Hand Detection System...")
    print("Available endpoints:")
    print("- GET  / : Main page")
    print("- POST /api/start : Start hand detection")
    print("- POST /api/stop : Stop hand detection")
    print("- GET  /api/status : Get detection status")
    print("- GET  /api/frame : Get current frame")
    print("- GET  /api/landmarks : Get hand landmarks")
    print("- POST /api/screenshot : Save screenshot")
    print("- GET  /health : Health check")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_camera()
    except Exception as e:
        print(f"Error starting server: {e}")
        stop_camera()
