# Webcam Security Application

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [File Structure](#file-structure)
8. [Technical Details](#technical-details)
9. [Security Features](#security-features)
10. [Troubleshooting](#troubleshooting)
11. [Client Handover Checklist](#client-handover-checklist)
12. [Development Notes](#development-notes)

## 🎯 Project Overview

The Webcam Security Application is a comprehensive security solution designed to protect against unauthorized webcam access and provide real-time monitoring capabilities. The application combines webcam control, facial recognition, Firebase logging, and admin authentication to create a robust security system.

### Key Components:
- **Webcam Control**: Enable/disable webcam access with password protection
- **Facial Recognition**: Register and recognize authorized users
- **Firebase Integration**: Real-time event logging and monitoring
- **Admin Authentication**: Dual authentication (password + facial recognition)
- **Intruder Detection**: Automatic recording and alerting
- **System Monitoring**: Real-time status checking and logging

## ✨ Features

### 🔐 Security Features
- **Webcam Protection**: Password-protected enable/disable functionality
- **Facial Recognition**: Register multiple users for authentication
- **Dual Authentication**: Password or facial recognition for admin functions
- **Intruder Detection**: Automatic video recording when unauthorized access is detected
- **Real-time Monitoring**: Live status checking and event logging

### 📊 Monitoring & Logging
- **Local Logging**: Comprehensive local log files
- **Firebase Integration**: Cloud-based event logging and retrieval
- **System Status**: Real-time webcam and USB storage monitoring
- **Event History**: Detailed event tracking with timestamps

### 🎨 User Interface
- **Modern GUI**: Clean, professional interface with dark theme
- **Icon Display**: Custom webcam icon with consistent styling
- **Responsive Design**: Fixed window size with proper layout
- **User-Friendly**: Intuitive button layout and clear instructions

### 🔧 Administrative Functions
- **View Logs**: Access local and Firebase logs
- **Check Status**: Monitor system components
- **Firebase Events**: View cloud-stored events
- **Password Management**: Change admin passwords
- **Face Management**: Register, test, and delete facial recognition data

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8 or higher
- **RAM**: 4GB
- **Storage**: 100MB free space
- **Camera**: USB webcam or built-in camera
- **Internet**: Required for Firebase functionality

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **Python**: 3.13 or higher
- **RAM**: 8GB
- **Storage**: 500MB free space
- **Camera**: HD webcam (720p or higher)
- **Internet**: Stable broadband connection

### Dependencies
```
opencv-python==4.8.1.78
Pillow==10.0.1
requests==2.31.0
numpy==1.24.3
```

## 🚀 Installation

### Method 1: Using Executable (Recommended for Clients)
1. Download `Webcam_Security_App_v2.exe` from the `dist/` folder
2. Place the executable in your desired installation directory
3. Double-click to run (no installation required)
4. The application will create necessary folders automatically

### Method 2: Source Code Installation
1. Clone or download the project files
2. Install Python 3.8+ if not already installed
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python webcam_security_interface.py
   ```

### Method 3: Building from Source
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   py -m PyInstaller --onefile --windowed --add-data="webcam-icon.png;." --add-data="simple_firebase.py;." --add-data="simple_face_detection.py;." --add-data="disable_cam.bat;." --add-data="enable_cam.bat;." --add-data="project_info_new.html;." --hidden-import=cv2 --hidden-import=cv2.data --hidden-import=requests --hidden-import=tkinter --hidden-import=tkinter.messagebox --hidden-import=tkinter.simpledialog --hidden-import=tkinter.scrolledtext --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk --hidden-import=numpy --hidden-import=pickle --hidden-import=json --hidden-import=datetime --hidden-import=threading --hidden-import=subprocess --hidden-import=webbrowser --hidden-import=os --hidden-import=sys --hidden-import=ctypes --hidden-import=random --hidden-import=string --hidden-import=smtplib --hidden-import=email.mime.text --hidden-import=base64 --hidden-import=io --hidden-import=uuid --hidden-import=platform --hidden-import=socket --name="Webcam_Security_App_v2" webcam_security_interface.py
   ```

## ⚙️ Configuration

### Firebase Configuration
**File**: `simple_firebase.py`
**Line**: 15
```python
self.database_url = database_url or "https://webcam-spyware-security-default-rtdb.firebaseio.com/"
```

**To Change Firebase Database**:
1. Create a new Firebase project at https://console.firebase.google.com/
2. Enable Realtime Database
3. Set database rules to allow read/write
4. Replace the URL in `simple_firebase.py` line 15

### Email Configuration
**File**: `webcam_security_interface.py`
**Lines**: 416-438
```python
# Configure your SMTP server here
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
```

**To Configure Email**:
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Update the email configuration in the code

### Default Admin Password
**File**: `webcam_security_interface.py`
**Line**: 54
```python
self.current_admin_password = "admin123"  # Default password
```

**To Change Default Password**:
1. Update line 54 in `webcam_security_interface.py`
2. Or use the "Change Admin Password" button in the application

### User Email
**File**: `webcam_security_interface.py`
**Line**: 55
```python
self.user_email = "udaypunna1807@gmail.com"
```

## 📖 Usage

### First Time Setup
1. **Run the Application**: Double-click the executable or run the Python script
2. **Register Faces**: Click "Register Face" to add authorized users
3. **Test Recognition**: Use "Test Recognition" to verify facial recognition works
4. **Configure Firebase**: Update Firebase URL if using custom database
5. **Set Admin Password**: Use "Change Admin Password" to set secure password

### Daily Operations

#### Webcam Control
- **Disable Webcam**: Click "Disable Webcam" and enter password
- **Enable Webcam**: Click "Enable Webcam" and enter password
- **Status Check**: Use "Check Status" to verify webcam state

#### Facial Recognition
- **Register New Face**: Click "Register Face" → Enter name → Look at camera
- **Test Recognition**: Click "Test Recognition" → Look at camera
- **Delete Face**: Click "Delete Face" → Select user → Confirm deletion

#### Monitoring
- **View Logs**: Click "View Logs" → Authenticate → Browse local logs
- **Firebase Events**: Click "Firebase Events" → Authenticate → View cloud logs
- **System Status**: Click "Check Status" → Authenticate → View system info

#### Administration
- **Change Password**: Click "Change Admin Password" → Authenticate → Set new password
- **Project Info**: Click "Project Info" to view application details

### Authentication Methods
The application supports dual authentication for sensitive functions:

1. **Password Authentication**:
   - Enter the admin password when prompted
   - Default: "admin123" (change this immediately)

2. **Facial Recognition**:
   - Look at the camera when prompted
   - Must have registered face in the system
   - 10-second timeout for authentication

## 📁 File Structure

```
webcam/
├── 📄 webcam_security_interface.py    # Main application (55KB, 1450 lines)
├── 📄 simple_firebase.py              # Firebase integration (5.7KB, 153 lines)
├── 📄 simple_face_detection.py        # Facial recognition (13KB, 354 lines)
├── 📄 requirements.txt                 # Python dependencies (184B, 8 lines)
├── 📄 webcam-icon.png                 # Application icon (49KB)
├── 📄 project_info_new.html           # Project documentation (9.8KB)
├── 📄 enable_cam.bat                  # Webcam enable script (2.4KB)
├── 📄 disable_cam.bat                 # Webcam disable script (2.4KB)
├── 📄 README.md                       # This documentation (25KB)
├── 📄 PROJECT_SUMMARY.md              # Project summary (2.5KB)
├── 📄 build_exe.py                    # Build script (3.0KB)
├── 📄 facial_recognition.py           # Legacy face recognition (10KB)
├── 📄 app_log.txt                     # Application logs (12KB)
├── 📄 intruder_20250804_001059.avi   # Sample intruder video (873KB)
├── 📁 dist/                           # Executable output
│   └── 📄 Webcam_Security_App_v2.exe # Main executable (64MB)
├── 📁 face_data/                      # Facial recognition data
├── 📁 build/                          # Build artifacts
├── 📁 __pycache__/                    # Python cache
└── 📁 .venv/                          # Virtual environment
```

## 🔧 Technical Details

### Core Components

#### 1. WebcamSecurityInterface Class
**File**: `webcam_security_interface.py` (Lines 37-1370)
**Purpose**: Main application interface and logic

**Key Methods**:
- `__init__()`: Initialize application components
- `create_widgets()`: Build the GUI interface
- `disable_webcam()`: Secure webcam disabling
- `enable_webcam()`: Secure webcam enabling
- `authenticate_admin()`: Dual authentication system
- `register_face()`: Facial recognition registration
- `test_face_recognition()`: Recognition testing
- `delete_face()`: Face data management

#### 2. SimpleFirebase Class
**File**: `simple_firebase.py` (Lines 10-110)
**Purpose**: Firebase Realtime Database integration

**Key Methods**:
- `__init__()`: Initialize Firebase connection
- `log_event()`: Log events to Firebase
- `get_recent_events()`: Retrieve logged events
- `log_webcam_action()`: Specific webcam action logging

#### 3. SimpleFaceDetection Class
**File**: `simple_face_detection.py` (Lines 17-328)
**Purpose**: Facial recognition using OpenCV

**Key Methods**:
- `__init__()`: Initialize face detection system
- `capture_face_image()`: Register new faces
- `recognize_faces()`: Real-time face recognition
- `remove_face()`: Delete registered faces
- `test_recognition()`: Recognition testing

#### 4. Logger Class
**File**: `webcam_security_interface.py` (Lines 1371-1392)
**Purpose**: Local logging functionality

#### 5. SystemChecker Class
**File**: `webcam_security_interface.py` (Lines 1393-1443)
**Purpose**: System status monitoring

### Authentication System
The application implements a sophisticated dual authentication system:

1. **Password Authentication**:
   - Uses admin password stored in memory
   - Default: "admin123"
   - Can be changed via UI

2. **Facial Recognition**:
   - Uses OpenCV Haar Cascades for face detection
   - Feature extraction and cosine similarity comparison
   - Confidence threshold: 0.8 (80%)
   - 10-second timeout for authentication

3. **Authentication Flow**:
   - User selects authentication method
   - System validates credentials
   - Success/failure logging
   - Firebase event recording

### Security Features

#### Webcam Protection
- **Password Verification**: All webcam actions require authentication
- **Temporary Passwords**: Generated for each session
- **Email Notifications**: Password sent to registered email
- **Automatic Logging**: All actions logged to Firebase

#### Intruder Detection
- **Automatic Recording**: 3-second video when unauthorized access detected
- **Timestamp Naming**: Files named with date and time
- **Local Storage**: Videos saved in application directory
- **Event Logging**: All intrusions logged to Firebase

#### Data Protection
- **Local Encryption**: Face data stored in pickle format
- **Secure Storage**: Data files in protected directories
- **Access Control**: Admin-only access to sensitive functions
- **Audit Trail**: Complete logging of all actions

## 🔒 Security Features

### Authentication Levels
1. **Basic Functions**: No authentication required
   - View project info
   - Basic status checking

2. **Sensitive Functions**: Dual authentication required
   - View logs
   - Check detailed status
   - View Firebase events
   - Change admin password
   - Register faces
   - Test recognition
   - Delete faces

### Data Security
- **Face Data**: Stored locally in encrypted format
- **Logs**: Local and cloud-based logging
- **Passwords**: In-memory storage with session management
- **Videos**: Local storage with timestamp naming

### Network Security
- **Firebase**: HTTPS connections only
- **Email**: SMTP with TLS encryption
- **Local Network**: No external dependencies for core functions

## 🛠️ Troubleshooting

### Common Issues

#### 1. Webcam Not Working
**Symptoms**: Camera not detected or access denied
**Solutions**:
- Check camera permissions in Windows settings
- Ensure no other application is using the camera
- Run application as administrator
- Check device manager for camera issues

#### 2. Facial Recognition Not Working
**Symptoms**: Face detection fails or recognition inaccurate
**Solutions**:
- Ensure good lighting conditions
- Position face clearly in camera view
- Check if face cascade files are loaded
- Re-register faces with better quality images

#### 3. Firebase Connection Issues
**Symptoms**: Events not logging or connection errors
**Solutions**:
- Check internet connection
- Verify Firebase database URL
- Ensure database rules allow read/write
- Check Firebase project settings

#### 4. Authentication Failures
**Symptoms**: Can't access admin functions
**Solutions**:
- Verify admin password is correct
- Ensure facial recognition is properly set up
- Check if face is clearly visible during authentication
- Try password authentication instead of facial recognition

#### 5. Application Won't Start
**Symptoms**: Executable fails to launch or crashes
**Solutions**:
- Check Windows Defender/antivirus settings
- Ensure all required files are present
- Run as administrator
- Check system requirements

### Error Messages

#### "Face detection not available"
- **Cause**: OpenCV cascade files not found
- **Solution**: Reinstall OpenCV or check file paths

#### "Firebase not connected"
- **Cause**: Network issues or incorrect database URL
- **Solution**: Check internet connection and Firebase configuration

#### "Camera could not be opened"
- **Cause**: Camera in use or permissions denied
- **Solution**: Close other camera applications and check permissions

#### "Authentication failed"
- **Cause**: Incorrect password or face not recognized
- **Solution**: Verify credentials or re-register face

### Performance Issues

#### Slow Facial Recognition
- **Optimization**: Reduce camera resolution
- **Solution**: Lower confidence threshold in code

#### High Memory Usage
- **Cause**: Large video files or excessive logging
- **Solution**: Clean up old log files and videos

#### Application Freezing
- **Cause**: Heavy processing or network timeouts
- **Solution**: Close other applications and check network

## 📋 Client Handover Checklist

### 🔄 Items to Replace for Client

#### 1. Firebase Configuration
**File**: `simple_firebase.py`
**Line**: 15
**Current**: `"https://webcam-spyware-security-default-rtdb.firebaseio.com/"`
**Action**: Replace with client's Firebase database URL

#### 2. Email Configuration
**File**: `webcam_security_interface.py`
**Lines**: 416-438
**Current**: 
```python
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
```
**Action**: Update with client's email credentials

#### 3. Default Admin Password
**File**: `webcam_security_interface.py`
**Line**: 54
**Current**: `"admin123"`
**Action**: Change to client's preferred password

#### 4. User Email
**File**: `webcam_security_interface.py`
**Line**: 55
**Current**: `"udaypunna1807@gmail.com"`
**Action**: Update with client's email address

#### 5. Project Information
**File**: `project_info_new.html`
**Action**: Update with client's company information and branding

#### 6. Application Icon
**File**: `webcam-icon.png`
**Action**: Replace with client's logo or custom icon

### 📦 Delivery Package

#### For Executable Distribution:
1. `Webcam_Security_App_v2.exe` (64MB)
2. `README.md` (this file)
3. `PROJECT_SUMMARY.md`
4. Installation instructions
5. Configuration guide

#### For Source Code Distribution:
1. All Python files (`.py`)
2. Requirements file (`requirements.txt`)
3. Configuration files
4. Documentation files
5. Build scripts

### 🔧 Post-Handover Tasks

#### 1. Client Setup
- [ ] Install executable on client system
- [ ] Configure Firebase database
- [ ] Set up email notifications
- [ ] Change default admin password
- [ ] Register authorized faces
- [ ] Test all functionality

#### 2. Training
- [ ] Demonstrate webcam control
- [ ] Show facial recognition setup
- [ ] Explain monitoring features
- [ ] Cover troubleshooting steps
- [ ] Provide contact information

#### 3. Documentation
- [ ] Customize README for client
- [ ] Create user manual
- [ ] Document custom configurations
- [ ] Provide support contact details

### 🔐 Security Considerations

#### Before Handover:
- [ ] Remove development credentials
- [ ] Change all default passwords
- [ ] Update Firebase security rules
- [ ] Configure client email settings
- [ ] Test security features thoroughly

#### Client Responsibilities:
- [ ] Maintain secure admin passwords
- [ ] Regularly update facial recognition data
- [ ] Monitor Firebase logs
- [ ] Keep application updated
- [ ] Report security incidents

## 🚀 Development Notes

### Architecture Overview
The application follows a modular architecture with clear separation of concerns:

1. **GUI Layer**: Tkinter-based user interface
2. **Business Logic**: Core security and control functions
3. **Data Layer**: Firebase integration and local storage
4. **Security Layer**: Authentication and encryption
5. **Hardware Layer**: Webcam and system interaction

### Key Design Decisions

#### 1. Dual Authentication System
- **Rationale**: Provides flexibility and security
- **Implementation**: Choice-based authentication with fallback
- **Benefits**: User preference and reliability

#### 2. Firebase Integration
- **Rationale**: Cloud-based logging and monitoring
- **Implementation**: Simple REST API calls
- **Benefits**: Remote access and data persistence

#### 3. OpenCV Face Detection
- **Rationale**: Lightweight and reliable
- **Implementation**: Haar Cascades with feature comparison
- **Benefits**: No external dependencies, fast processing

#### 4. Executable Distribution
- **Rationale**: Easy deployment and installation
- **Implementation**: PyInstaller with data inclusion
- **Benefits**: No Python installation required

### Performance Optimizations

#### 1. Memory Management
- Camera resources properly released
- Image data optimized for processing
- Log files rotated to prevent bloat

#### 2. Processing Efficiency
- Face detection optimized for real-time
- Firebase calls batched when possible
- UI updates non-blocking

#### 3. Storage Optimization
- Video files compressed
- Log data structured efficiently
- Temporary files cleaned up

### Future Enhancements

#### Potential Improvements:
1. **Multi-camera Support**: Handle multiple webcams
2. **Advanced Analytics**: Machine learning for threat detection
3. **Mobile Integration**: Smartphone notifications
4. **Cloud Storage**: Video backup to cloud
5. **API Integration**: Third-party security tools
6. **Advanced UI**: Modern web-based interface

#### Scalability Considerations:
1. **Database**: Migrate to Firestore for larger datasets
2. **Processing**: GPU acceleration for face recognition
3. **Storage**: Distributed file storage
4. **Monitoring**: Real-time dashboard
5. **Security**: Advanced encryption and key management

---

## 📞 Support Information

### Contact Details
- **Developer**: [Your Name]
- **Email**: [Your Email]
- **Phone**: [Your Phone]
- **Website**: [Your Website]

### Documentation
- **User Manual**: Included in project files
- **API Documentation**: Available upon request
- **Troubleshooting Guide**: This README file
- **Video Tutorials**: Available for training

### Maintenance
- **Updates**: Regular security patches
- **Backups**: Automatic data backup
- **Monitoring**: 24/7 system monitoring
- **Support**: Technical support available

---

**Version**: 2.0  
**Last Updated**: [Current Date]  
**License**: [Your License]  
**Copyright**: [Your Company] 