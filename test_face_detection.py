#!/usr/bin/env python3
"""
Simple test script to verify face detection works in executable
"""

from simple_face_detection import SimpleFaceDetection

print("🧠 Testing Face Detection System...")
print("=" * 50)

# Initialize face detection
fd = SimpleFaceDetection()

# Check if face cascade is loaded
if fd.face_cascade is not None:
    print("✅ Face cascade loaded successfully!")
    print("✅ Face detection system is ready")
else:
    print("❌ Face cascade failed to load")
    print("❌ Face detection system is NOT working")

# Test basic functionality
try:
    known_faces = fd.get_known_faces()
    print(f"📋 Currently registered faces: {len(known_faces)}")
    for face in known_faces:
        print(f"  - {face}")
    
    print("\n🎯 Face detection system test completed!")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")

input("Press Enter to exit...")
