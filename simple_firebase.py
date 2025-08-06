#!/usr/bin/env python3
"""
Simple Firebase Connection using Realtime Database
Much easier to set up than Firestore
"""

import requests
import json
import datetime
import time

class SimpleFirebase:
    def __init__(self, database_url=None):
        """Initialize simple Firebase connection"""
        # Default database URL (you can change this)
        self.database_url = database_url or "https://webcam-spyware-security-c7629-default-rtdb.firebaseio.com/"
        self.is_connected = False
        self.test_connection()
    
    def test_connection(self):
        """Test if we can connect to Firebase"""
        try:
            # Try to read from database
            response = requests.get(f"{self.database_url}/.json")
            if response.status_code == 200:
                self.is_connected = True
                print("✅ Simple Firebase connected successfully!")
                return True
            else:
                print(f"❌ Firebase connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Firebase connection error: {e}")
            return False
    
    def log_event(self, event_type, description, severity="INFO", additional_data=None):
        """Log an event to Firebase"""
        if not self.is_connected:
            print("⚠️ Firebase not connected, logging locally only")
            return False
        
        try:
            event_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "event_type": event_type,
                "description": description,
                "severity": severity,
                "additional_data": additional_data or {}
            }
            
            # Write to Firebase
            response = requests.post(
                f"{self.database_url}/events.json",
                json=event_data
            )
            
            if response.status_code == 200:
                print(f"✅ Event logged: {event_type}")
                return True
            else:
                print(f"❌ Failed to log event: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error logging event: {e}")
            return False
    
    def get_recent_events(self, limit=10):
        """Get recent events from Firebase"""
        if not self.is_connected:
            print("⚠️ Firebase not connected")
            return []
        
        try:
            response = requests.get(f"{self.database_url}/events.json")
            if response.status_code == 200:
                data = response.json()
                if data:
                    # Convert to list and sort by timestamp
                    events = []
                    for key, event in data.items():
                        event['id'] = key
                        events.append(event)
                    
                    # Sort by timestamp (newest first)
                    events.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
                    return events[:limit]
                else:
                    return []
            else:
                print(f"❌ Failed to get events: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting events: {e}")
            return []
    
    def log_webcam_action(self, action, success=True, user="system"):
        """Log webcam actions specifically"""
        event_type = f"WEBCAM_{action.upper()}"
        description = f"Webcam {action} {'successful' if success else 'failed'}"
        
        return self.log_event(
            event_type,
            description,
            "INFO" if success else "ERROR",
            {"user": user, "action": action}
        )

# Test the simple Firebase connection
def test_simple_firebase():
    print("🔥 Testing Simple Firebase Connection...")
    print("=" * 50)
    
    firebase = SimpleFirebase()
    
    if firebase.is_connected:
        print("✅ Simple Firebase is working!")
        
        # Test logging an event
        print("\n📝 Testing event logging...")
        firebase.log_event("TEST", "Simple Firebase test successful", "INFO")
        
        # Test webcam action logging
        print("\n📹 Testing webcam action logging...")
        firebase.log_webcam_action("disable", True, "test_user")
        firebase.log_webcam_action("enable", True, "test_user")
        
        # Get recent events
        print("\n📖 Getting recent events...")
        events = firebase.get_recent_events(5)
        print(f"Found {len(events)} recent events:")
        for event in events:
            timestamp = event.get('timestamp', 'Unknown')
            event_type = event.get('event_type', 'Unknown')
            description = event.get('description', 'No description')
            print(f"  [{timestamp}] {event_type}: {description}")
        
        print("\n🎉 Simple Firebase test completed successfully!")
        return True
    else:
        print("❌ Simple Firebase connection failed")
        print("\n🔧 To fix this:")
        print("1. Go to Firebase Console: https://console.firebase.google.com/")
        print("2. Select your project: webcam-spyware-security")
        print("3. Click 'Realtime Database' in the left sidebar")
        print("4. Click 'Create database'")
        print("5. Choose 'Start in test mode'")
        print("6. Copy the database URL and update it in the code")
        return False

if __name__ == "__main__":
    test_simple_firebase() 