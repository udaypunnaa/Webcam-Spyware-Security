#!/usr/bin/env python3
"""
Simple Face Detection and Recognition using OpenCV
Uses OpenCV's built-in face detection and basic face comparison
"""

import cv2
import numpy as np
import os
import sys
import pickle
import datetime
import json
from PIL import Image

class SimpleFaceDetection:
    def __init__(self, data_dir="face_data"):
        """Initialize face detection system"""
        self.data_dir = data_dir
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_data_file = os.path.join(data_dir, "face_encodings.pkl")
        self.face_names_file = os.path.join(data_dir, "face_names.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load OpenCV face detection cascade
        try:
            cascade_path = None
            self.face_cascade = None
            
            # Get the correct base directory
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Try multiple cascade paths in order of preference
            cascade_paths = [
                # 1. Local project directory (for executable)
                os.path.join(base_dir, 'haarcascade_frontalface_default.xml'),
                # 2. PyInstaller temporary directory
                os.path.join(getattr(sys, '_MEIPASS', ''), 'haarcascade_frontalface_default.xml') if getattr(sys, 'frozen', False) else None,
                # 3. Standard OpenCV path (for development)
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml',
            ]
            
            # Filter out None paths
            cascade_paths = [path for path in cascade_paths if path is not None]
            
            for path in cascade_paths:
                print(f"[DEBUG] Trying cascade path: {path}")
                if os.path.exists(path):
                    print(f"[DEBUG] File exists, attempting to load...")
                    self.face_cascade = cv2.CascadeClassifier(path)
                    if not self.face_cascade.empty():
                        print(f"✅ Face cascade loaded successfully from: {path}")
                        cascade_path = path
                        break
                    else:
                        print(f"⚠️ Cascade file exists but failed to load: {path}")
                else:
                    print(f"⚠️ Cascade file not found: {path}")
            
            if self.face_cascade is None or self.face_cascade.empty():
                print("❌ Warning: Could not load face cascade classifier from any location")
                self.face_cascade = None
                
        except Exception as e:
            print(f"❌ Error loading face cascade: {e}")
            self.face_cascade = None
        
        # Load existing face data
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load previously saved face encodings and names"""
        try:
            if os.path.exists(self.face_data_file):
                with open(self.face_data_file, 'rb') as f:
                    self.known_face_encodings = pickle.load(f)
                print(f"✅ Loaded {len(self.known_face_encodings)} known face encodings")
            
            if os.path.exists(self.face_names_file):
                with open(self.face_names_file, 'r') as f:
                    self.known_face_names = json.load(f)
                print(f"✅ Loaded {len(self.known_face_names)} known face names")
                
        except Exception as e:
            print(f"⚠️ Error loading face data: {e}")
            self.known_face_encodings = []
            self.known_face_names = []
    
    def save_known_faces(self):
        """Save face encodings and names to files"""
        try:
            with open(self.face_data_file, 'wb') as f:
                pickle.dump(self.known_face_encodings, f)
            
            with open(self.face_names_file, 'w') as f:
                json.dump(self.known_face_names, f)
            
            print("✅ Face data saved successfully")
            return True
        except Exception as e:
            print(f"❌ Error saving face data: {e}")
            return False
    
    def extract_face_features(self, face_img):
        """Extract basic features from a face image"""
        # Resize to standard size
        face_img = cv2.resize(face_img, (100, 100))
        
        # Convert to grayscale
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization
        gray = cv2.equalizeHist(gray)
        
        # Flatten and normalize
        features = gray.flatten().astype(np.float32) / 255.0
        
        return features
    
    def compare_faces(self, face1_features, face2_features, threshold=0.8):
        """Compare two face feature vectors"""
        # Calculate cosine similarity
        similarity = np.dot(face1_features, face2_features) / (
            np.linalg.norm(face1_features) * np.linalg.norm(face2_features)
        )
        return similarity > threshold
    
    def capture_face_image(self, name, duration=5):
        """Capture a face image for registration"""
        if self.face_cascade is None:
            print("❌ Face detection not available - cascade classifier not loaded")
            print("[DEBUG] Please ensure haarcascade_frontalface_default.xml is available")
            return False
            
        print(f"📸 Capturing face image for {name}...")
        print("Please look at the camera and press 'q' to stop early")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Could not open camera")
            return False
        
        # Set camera properties for better quality
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        start_time = datetime.datetime.now()
        best_face_features = None
        best_face_image = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to capture frame")
                break
            
            # Flip the frame horizontally for a later selfie-view display
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Extract face features
                face_img = frame[y:y+h, x:x+w]
                if face_img.size > 0:
                    best_face_features = self.extract_face_features(face_img)
                    best_face_image = frame.copy()
            
            # Add timer and instructions
            elapsed = (datetime.datetime.now() - start_time).seconds
            remaining = max(0, duration - elapsed)
            
            cv2.putText(frame, f"Time: {remaining}s", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Registering: {name}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to stop early", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Face Registration', frame)
            
            # Check for 'q' key or timeout
            if cv2.waitKey(1) & 0xFF == ord('q') or elapsed >= duration:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if best_face_features is not None:
            # Save the face image
            image_path = os.path.join(self.data_dir, f"{name}.jpg")
            cv2.imwrite(image_path, best_face_image)
            
            # Add to known faces
            self.known_face_encodings.append(best_face_features)
            self.known_face_names.append(name)
            
            # Save the data
            self.save_known_faces()
            
            print(f"✅ Face registered successfully for {name}")
            return True
        else:
            print("❌ No face detected during capture")
            return False
    
    def recognize_faces(self, frame, confidence_threshold=0.8):
        """Recognize faces in a frame"""
        if self.face_cascade is None:
            return [], []
            
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        face_locations = []
        face_names = []
        
        for (x, y, w, h) in faces:
            face_locations.append((y, x+w, y+h, x))
            
            # Extract face features
            face_img = frame[y:y+h, x:x+w]
            if face_img.size > 0:
                face_features = self.extract_face_features(face_img)
                
                # Compare with known faces
                name = "Unknown"
                for i, known_features in enumerate(self.known_face_encodings):
                    if self.compare_faces(face_features, known_features, confidence_threshold):
                        name = self.known_face_names[i]
                        break
                
                face_names.append(name)
            else:
                face_names.append("Unknown")
        
        return face_locations, face_names
    
    def get_known_faces(self):
        """Get list of registered face names"""
        return self.known_face_names.copy()
    
    def remove_face(self, name):
        """Remove a registered face"""
        try:
            if name in self.known_face_names:
                index = self.known_face_names.index(name)
                self.known_face_names.pop(index)
                self.known_face_encodings.pop(index)
                
                # Remove image file
                image_path = os.path.join(self.data_dir, f"{name}.jpg")
                if os.path.exists(image_path):
                    os.remove(image_path)
                
                self.save_known_faces()
                print(f"✅ Removed face registration for {name}")
                return True
            else:
                print(f"❌ Face '{name}' not found")
                return False
        except Exception as e:
            print(f"❌ Error removing face: {e}")
            return False
    
    def test_recognition(self, duration=10):
        """Test face recognition in real-time"""
        if self.face_cascade is None:
            print("❌ Face detection not available - cascade classifier not loaded")
            return
            
        print("🔍 Testing face recognition...")
        print("Press 'q' to stop")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Could not open camera")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        start_time = datetime.datetime.now()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            # Recognize faces
            face_locations, face_names = self.recognize_faces(frame)
            
            # Draw results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw rectangle
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Draw name
                cv2.putText(frame, name, (left, top - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Add info
            elapsed = (datetime.datetime.now() - start_time).seconds
            cv2.putText(frame, f"Time: {elapsed}s", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to stop", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Face Recognition Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Face recognition test completed")

def test_simple_face_detection():
    """Test the simple face detection system"""
    print("🧠 Testing Simple Face Detection System...")
    print("=" * 50)
    
    fd = SimpleFaceDetection()
    
    print(f"📋 Known faces: {fd.get_known_faces()}")
    
    # Test registration
    name = input("Enter name to register (or press Enter to skip): ").strip()
    if name:
        if fd.capture_face_image(name):
            print(f"✅ {name} registered successfully")
        else:
            print(f"❌ Failed to register {name}")
    
    # Test recognition
    if fd.get_known_faces():
        test = input("Test recognition? (y/n): ").lower().strip()
        if test == 'y':
            fd.test_recognition()
    else:
        print("⚠️ No faces registered for testing")

if __name__ == "__main__":
    test_simple_face_detection() 