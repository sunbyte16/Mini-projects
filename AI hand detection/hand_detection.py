import cv2
import numpy as np
from datetime import datetime
import time

class HandDetector:
    def __init__(self):
        # Initialize parameters for skin color detection
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Load pre-trained hand cascade classifier (if available)
        try:
            self.hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_hand.xml')
        except:
            self.hand_cascade = None
            print("Hand cascade classifier not available, using color-based detection")
        
        # Initialize hands attribute for compatibility
        self.hands = None
        
    def find_hands(self, img, draw=True):
        """Detect hands using improved color-based detection and contour analysis"""
        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Improved skin color range - more inclusive
        lower_skin1 = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin1 = np.array([20, 255, 255], dtype=np.uint8)
        lower_skin2 = np.array([170, 20, 70], dtype=np.uint8)
        upper_skin2 = np.array([180, 255, 255], dtype=np.uint8)
        
        # Create masks for different skin tones
        mask1 = cv2.inRange(hsv, lower_skin1, upper_skin1)
        mask2 = cv2.inRange(hsv, lower_skin2, upper_skin2)
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.GaussianBlur(mask, (5,5), 0)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        hand_count = 0
        if contours and draw:
            # Sort contours by area and process the largest ones
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            
            for contour in contours[:2]:  # Process up to 2 hands
                area = cv2.contourArea(contour)
                # Lowered threshold for better detection
                if area > 500:  # Reduced minimum area threshold
                    hand_count += 1
                    
                    # Draw bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    
                    # Draw contour
                    cv2.drawContours(img, [contour], -1, (0, 0, 255), 2)
                    
                    # Draw convex hull
                    hull = cv2.convexHull(contour)
                    cv2.drawContours(img, [hull], -1, (255, 0, 0), 2)
                    
                    # Calculate and draw palm center
                    M = cv2.moments(contour)
                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.circle(img, (cx, cy), 10, (0, 255, 255), -1)
                        
                        # Add hand label
                        cv2.putText(img, f'Hand {hand_count}', (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        
                        # Add area info
                        cv2.putText(img, f'Area: {int(area)}', (x, y+h+20), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Add detection info
        cv2.putText(img, f'Hands: {hand_count}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f'Contours: {len(contours)}', (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        return img, hand_count
    
    def detect_gesture(self, img):
        """Detect hand gestures using contour analysis"""
        # Convert to HSV and create mask
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
        
        # Apply morphological operations
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        gesture = 'No Hand'
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(max_contour)
            
            if area > 1000:
                # Calculate convex hull and defects
                hull = cv2.convexHull(max_contour, returnPoints=False)
                defects = cv2.convexityDefects(max_contour, hull)
                
                # Count fingers based on defects
                finger_count = 0
                if defects is not None:
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        if d > 10000:  # threshold for defect depth
                            finger_count += 1
                    
                    finger_count = min(finger_count + 1, 5)  # Add 1 for the base finger
                    gesture = f'Fingers: {finger_count}'
                
                # Display gesture
                cv2.putText(img, gesture, (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return gesture, img
    
    def get_hand_landmarks(self, img):
        """Get hand landmarks using contour analysis (simplified version)"""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
        
        # Apply morphological operations
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=1)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        landmarks_list = []
        if contours:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:
                    # Get contour points as landmarks
                    landmarks = []
                    for point in contour:
                        x, y = point[0]
                        landmarks.append([x / img.shape[1], y / img.shape[0], 0])  # Normalize coordinates
                    
                    landmarks_list.append(landmarks)
        
        return landmarks_list

def main():
    """Main function to run hand detection"""
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    detector = HandDetector()
    
    # FPS calculation variables
    fps_counter = 0
    fps_start_time = time.time()
    fps = 0
    
    print("Hand Detection System Started")
    print("Controls:")
    print("- Press 'q' to quit")
    print("- Press 's' to save screenshot")
    print("- Press 'g' to toggle gesture detection")
    
    gesture_mode = True
    
    try:
        while True:
            success, img = cap.read()
            if not success:
                print("Failed to grab frame")
                break
                
            # Flip the image horizontally for a later selfie-view display
            img = cv2.flip(img, 1)
            
            # Find and draw hands
            img, hand_count = detector.find_hands(img)
            
            # Detect gesture if enabled
            if gesture_mode:
                gesture, img = detector.detect_gesture(img)
            
            # Calculate FPS
            fps_counter += 1
            if time.time() - fps_start_time >= 1.0:
                fps = fps_counter
                fps_counter = 0
                fps_start_time = time.time()
            
            # Display FPS and hand count
            cv2.putText(img, f'FPS: {fps}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, f'Hands: {hand_count}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display mode
            mode_text = "Gesture Mode: ON" if gesture_mode else "Gesture Mode: OFF"
            cv2.putText(img, mode_text, (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Show image
            cv2.imshow('Hand Detection', img)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Quit
                break
            elif key == ord('s'):  # Save screenshot
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'hand_detection_{timestamp}.jpg'
                cv2.imwrite(filename, img)
                print(f"Screenshot saved as {filename}")
            elif key == ord('g'):  # Toggle gesture mode
                gesture_mode = not gesture_mode
                print(f"Gesture mode: {'ON' if gesture_mode else 'OFF'}")
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        print("Hand Detection System Stopped")

if __name__ == "__main__":
    main()
