import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import subprocess
import webbrowser
import os
import datetime
import threading
import time
import sys
import ctypes
import random
import string
import smtplib
from email.mime.text import MIMEText
import cv2
import datetime
import base64
from io import BytesIO
from PIL import Image, ImageTk
from simple_firebase import SimpleFirebase
from simple_face_detection import SimpleFaceDetection


if hasattr(sys, '_MEIPASS'):
    sys.path.append(os.path.join(sys._MEIPASS, 'cv2'))

def is_admin():
    """Check if the current process has administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the program with administrator privileges"""
    try:
        if not is_admin():
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            return True
    except:
        pass
    return False

class WebcamSecurityInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam Spyware Security")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Configure black background
        self.root.configure(bg="#000000")
        
        # Initialize components
        self.logger = Logger()
        self.system_checker = SystemChecker()
        self.firebase_manager = SimpleFirebase()  # Initialize Firebase
        self.face_recognition = SimpleFaceDetection()  # Initialize facial recognition
        self.current_admin_password = "admin123"  # Default password
        self.user_email = "lankashraddha6@gmail.com"
        self._webcam_action_password = None  # Temporary password for enable/disable
        # Defensive: release webcam if open at startup
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                cap.release()
        except Exception as e:
            print(f"Webcam check at startup failed: {e}")
        # Removed face_encoding_file and admin_face_encoding
        
        # Get the correct base directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            self.base_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Log application start
        self.logger.log(f"Webcam Security Interface started from: {self.base_dir}")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Configure grid weights for main frame
        main_frame.columnconfigure(0, weight=1)  # Left side (icon area)
        main_frame.columnconfigure(1, weight=1)  # Right side (buttons)
        main_frame.rowconfigure(0, weight=0)     # Top section (Project Info)
        main_frame.rowconfigure(1, weight=0)     # Title section
        main_frame.rowconfigure(2, weight=1)     # Middle section
        main_frame.rowconfigure(3, weight=0)     # Bottom section
        
        # --- Top Section ---
        # Project Info button at top center
        btn_project_info = tk.Button(
            main_frame, 
            text="Project Info", 
            command=self.open_project_info,
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8
        )
        btn_project_info.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Main title
        title_label = tk.Label(
            main_frame,
            text="Webcam Spyware Security",
            font=("Arial", 28, "bold"),
            fg="#FFFFFF",
            bg="#000000"
        )
        title_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # --- Middle Section ---
        # Left side - Icon area
        icon_frame = tk.Frame(main_frame, bg="#333333", width=300, height=300)
        icon_frame.grid(row=2, column=0, padx=(0, 20), sticky="nsew")
        icon_frame.grid_propagate(False)  # Maintain fixed size
        icon_frame.configure(width=300, height=300)  # Ensure proper sizing
        
        # Load and display webcam icon
        try:
            # Try to load the webcam icon image
            icon_path = os.path.join(self.base_dir, "webcam-icon.png")
            
            if os.path.exists(icon_path):
                try:
                    # Load image
                    image = Image.open(icon_path)
                    
                    # Convert to RGB if necessary
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    # Resize image to fit the icon area with high quality
                    image = image.resize((200, 200), Image.Resampling.LANCZOS)
                    
                    # Create PhotoImage for Tkinter
                    photo = ImageTk.PhotoImage(image)
                    
                    # Create label with the image
                    icon_label = tk.Label(
                        icon_frame,
                        image=photo,
                        bg="#333333"
                    )
                    icon_label.image = photo  # Keep a reference to prevent garbage collection
                    icon_label.place(relx=0.5, rely=0.5, anchor="center")
                    
                    # Add a subtle border around the icon
                    icon_frame.configure(relief=tk.RAISED, bd=2)
                    
                    print(f"Successfully loaded webcam icon from: {icon_path}")
                    
                except Exception as e:
                    print(f"Could not load image: {e}")
                    # Fallback to emoji icon
                    icon_label = tk.Label(
                        icon_frame,
                        text="📷",
                        font=("Arial", 48),
                        fg="#FFFFFF",
                        bg="#333333"
                    )
                    icon_label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                print(f"Icon file not found at: {icon_path}")
                # Fallback to emoji icon if file doesn't exist
                icon_label = tk.Label(
                    icon_frame,
                    text="📷",
                    font=("Arial", 48),
                    fg="#FFFFFF",
                    bg="#333333"
                )
                icon_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Error loading icon: {e}")
            # Final fallback to emoji
            icon_label = tk.Label(
                icon_frame,
                text="📷",
                font=("Arial", 48),
                fg="#FFFFFF",
                bg="#333333"
            )
            icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Right side - Vertical buttons
        buttons_frame = tk.Frame(main_frame, bg="#000000")
        buttons_frame.grid(row=2, column=1, padx=(20, 0), sticky="nsew")
        
        # Configure buttons frame grid
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.rowconfigure(0, weight=1)
        buttons_frame.rowconfigure(1, weight=1)
        buttons_frame.rowconfigure(2, weight=1)
        buttons_frame.rowconfigure(3, weight=1) # Firebase Events button
        buttons_frame.rowconfigure(4, weight=1) # Register Face button
        buttons_frame.rowconfigure(5, weight=1) # Test Recognition button
        buttons_frame.rowconfigure(6, weight=1) # Delete Face button
        
        # View Logs button
        btn_view_logs = tk.Button(
            buttons_frame,
            text="View Logs",
            command=self.view_logs,
            font=("Arial", 12, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_view_logs.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Check Status button
        btn_check_status = tk.Button(
            buttons_frame,
            text="Check Status",
            command=self.check_status,
            font=("Arial", 12, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_check_status.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        
        # Change Admin Password button
        btn_change_password = tk.Button(
            buttons_frame,
            text="Change Admin Password",
            command=self.change_admin_password,
            font=("Arial", 12, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_change_password.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        
        # Firebase Events button
        btn_firebase_events = tk.Button(
            buttons_frame,
            text="Firebase Events",
            command=self.view_firebase_events,
            font=("Arial", 12, "bold"),
            bg="#FFA500",
            fg="#000000",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_firebase_events.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        
        # Facial Recognition buttons
        btn_register_face = tk.Button(
            buttons_frame,
            text="Register Face",
            command=self.register_face,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_register_face.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        
        btn_test_recognition = tk.Button(
            buttons_frame,
            text="Test Recognition",
            command=self.test_face_recognition,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_test_recognition.grid(row=5, column=0, pady=(0, 20), sticky="ew")
        
        btn_delete_face = tk.Button(
            buttons_frame,
            text="Delete Face",
            command=self.delete_face,
            font=("Arial", 12, "bold"),
            bg="#FF5722",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_delete_face.grid(row=6, column=0, pady=(0, 20), sticky="ew")
        
        # --- Bottom Section ---
        # Bottom buttons frame
        bottom_frame = tk.Frame(main_frame, bg="#000000")
        bottom_frame.grid(row=3, column=0, columnspan=2, pady=(30, 0), sticky="ew")
        
        # Configure bottom frame grid
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        
        # Disable button (left)
        btn_disable = tk.Button(
            bottom_frame,
            text="Disable",
            command=self.disable_webcam,
            font=("Arial", 16, "bold"),
            bg="#FF4D4D",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=40,
            pady=20
        )
        btn_disable.grid(row=0, column=0, padx=(0, 20), sticky="ew")
        
        # Enable button (right)
        btn_enable = tk.Button(
            bottom_frame,
            text="Enable",
            command=self.enable_webcam,
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=40,
            pady=20
        )
        btn_enable.grid(row=0, column=1, padx=(20, 0), sticky="ew")
    
    # --- Event Handlers ---
    def open_project_info(self):
        """Handle Project Info button click"""
        print("Project Info button clicked")
        self.logger.log("Project Info button clicked")
        try:
            # Try to open project_info_new.html first, then fallback to project_info.html
            project_info_path = os.path.join(self.base_dir, "project_info_new.html")
            if not os.path.exists(project_info_path):
                project_info_path = os.path.join(self.base_dir, "project_info.html")
            
            if os.path.exists(project_info_path):
                webbrowser.open(f"file://{project_info_path}")
                self.logger.log("Project info opened successfully")
            else:
                messagebox.showinfo("Project Info", "Project information file not found.")
                self.logger.log("Project info file not found")
        except Exception as e:
            print(f"Error opening project info: {e}")
            self.logger.log(f"Error opening project info: {e}")
            messagebox.showinfo("Project Info", "Project information not available.")
    
    def view_logs(self):
        # Authenticate user (password or face recognition)
        if not self.authenticate_admin("view logs"):
            return
        print("View Logs button clicked")
        self.logger.log("View Logs button clicked")
        self.show_logs_window()
    
    def check_status(self):
        # Authenticate user (password or face recognition)
        if not self.authenticate_admin("check status"):
            return
        print("Check Status button clicked")
        self.logger.log("Check Status button clicked")
        self.show_status_window()
    
    def view_firebase_events(self):
        """Handle Firebase Events button click"""
        # Authenticate user (password or face recognition)
        if not self.authenticate_admin("view Firebase events"):
            return
        
        print("Firebase Events button clicked")
        self.logger.log("Firebase Events button clicked")
        self.show_firebase_events_window()
    
    def change_admin_password(self):
        # Authenticate user (password or face recognition)
        if not self.authenticate_admin("change admin password"):
            return
        print("Change Admin Password button clicked")
        self.logger.log("Change Admin Password button clicked")
        self.show_password_change_dialog()
    
    def _generate_password(self, length=8):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def _send_email(self, to_email, password):
        # Configure your SMTP server here
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'lankashraddha6@gmail.com'
        smtp_pass = 'cgzs hzyn xfum kpvp'
        from_email = smtp_user
        subject = 'Your Webcam Security Verification Password'
        body = f'Your verification password is: {password}'
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(from_email, [to_email], msg.as_string())
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def _record_intruder_video(self, duration=3):
        print("[Intruder] Recording started after wrong password.")
        self.logger.log("Intruder video recording started after wrong password.")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Webcam not accessible for intruder recording.")
            return
        # Read the first frame to get the size
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from webcam for intruder video.")
            cap.release()
            return
        height, width = frame.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        out = cv2.VideoWriter(f'intruder_{timestamp}.avi', fourcc, 20.0, (width, height))
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).seconds < duration:
            out.write(frame)
            ret, frame = cap.read()
            if not ret:
                break
        cap.release()
        out.release()
        print(f"Intruder video saved as intruder_{timestamp}.avi")

    # Remove _load_face_encoding, _save_face_encoding, register_face, _verify_face methods

    def disable_webcam(self):
        # Remove face verification requirement
        # Password verification for webcam action
        if not self.user_email:
            messagebox.showerror("Error", "No email address set. Please contact admin to set your email address.")
            return
        # Generate and send password
        self._webcam_action_password = self._generate_password()
        if not self._send_email(self.user_email, self._webcam_action_password):
            messagebox.showerror("Error", "Failed to send verification email. Please try again.")
            return
        # Prompt for password
        user_input = simpledialog.askstring(
            "Verification Required",
            f"A verification password has been sent to {self.user_email}.\nEnter the password to disable the webcam:",
            show="*"
        )
        if user_input != self._webcam_action_password:
            messagebox.showerror("Error", "Incorrect verification password. Webcam will not be disabled.")
            self.logger.log("Failed webcam disable attempt - incorrect verification password")
            # Log security event to Firebase
            self.firebase_manager.log_event(
                "AUTH_FAILURE", 
                "Failed webcam disable attempt - incorrect verification password",
                "WARNING",
                {"action": "disable_webcam", "email": self.user_email}
            )
            self._record_intruder_video()
            return
        self._webcam_action_password = None
        print("Webcam Disabled")
        self.logger.log("Webcam disable button clicked")
        
        # Check if we have admin privileges
        if not is_admin():
            response = messagebox.askyesno(
                "Administrator Privileges Required", 
                "This operation requires administrator privileges.\n\nWould you like to restart the application with administrator privileges?"
            )
            if response:
                run_as_admin()
                return
            else:
                messagebox.showinfo("Info", "Operation cancelled. Webcam disable requires administrator privileges.")
                return
        
        try:
            # Try to run disable_cam.bat if it exists
            disable_script = os.path.join(self.base_dir, "disable_cam.bat")
            if os.path.exists(disable_script):
                # Run the batch file
                result = subprocess.run(
                    ["cmd", "/c", disable_script], 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    cwd=self.base_dir
                )
                
                if result.returncode == 0:
                    messagebox.showinfo(
                        "Webcam Disabled", 
                        "Webcam has been disabled successfully!\n\n"
                        "The webcam should now be disabled immediately.\n"
                        "Try opening the Camera app to test.\n\n"
                        "If the camera still works:\n"
                        "• Close and reopen the camera app\n"
                        "• Try a different camera application\n"
                        "• Check Device Manager for camera status\n\n"
                        "The changes are now active without requiring a restart."
                    )
                    self.logger.log("Webcam disabled successfully")
                    # Log successful webcam disable to Firebase
                    self.firebase_manager.log_event(
                        "WEBCAM_DISABLED", 
                        "Webcam disabled successfully",
                        "INFO",
                        {"method": "batch_script", "return_code": result.returncode}
                    )
                else:
                    error_msg = result.stderr if result.stderr else "Unknown error occurred"
                    messagebox.showerror("Error", f"Failed to disable webcam.\n\nError: {error_msg}")
                    self.logger.log(f"Failed to disable webcam: {error_msg}")
                    # Log failed webcam disable to Firebase
                    self.firebase_manager.log_event(
                        "WEBCAM_DISABLE_FAILED", 
                        f"Failed to disable webcam: {error_msg}",
                        "ERROR",
                        {"method": "batch_script", "return_code": result.returncode, "error": error_msg}
                    )
            else:
                messagebox.showinfo("Info", "Disable script not found. Please ensure 'disable_cam.bat' is in the same directory as the application.")
                self.logger.log("Disable script not found")
        except Exception as e:
            print(f"Error disabling webcam: {e}")
            self.logger.log(f"Error disabling webcam: {e}")
            messagebox.showerror("Error", f"Failed to disable webcam: {e}")
    
    def enable_webcam(self):
        # Remove face verification requirement
        # Password verification for webcam action
        if not self.user_email:
            messagebox.showerror("Error", "No email address set. Please contact admin to set your email address.")
            return
        # Generate and send password
        self._webcam_action_password = self._generate_password()
        if not self._send_email(self.user_email, self._webcam_action_password):
            messagebox.showerror("Error", "Failed to send verification email. Please try again.")
            return
        # Prompt for password
        user_input = simpledialog.askstring(
            "Verification Required",
            f"A verification password has been sent to {self.user_email}.\nEnter the password to enable the webcam:",
            show="*"
        )
        if user_input != self._webcam_action_password:
            messagebox.showerror("Error", "Incorrect verification password. Webcam will not be enabled.")
            self.logger.log("Failed webcam enable attempt - incorrect verification password")
            # Log security event to Firebase
            self.firebase_manager.log_event(
                "AUTH_FAILURE", 
                "Failed webcam enable attempt - incorrect verification password",
                "WARNING",
                {"action": "enable_webcam", "email": self.user_email}
            )
            self._record_intruder_video()
            return
        self._webcam_action_password = None
        print("Webcam Enabled")
        self.logger.log("Webcam enable button clicked")
        
        # Check if we have admin privileges
        if not is_admin():
            response = messagebox.askyesno(
                "Administrator Privileges Required", 
                "This operation requires administrator privileges.\n\nWould you like to restart the application with administrator privileges?"
            )
            if response:
                run_as_admin()
                return
            else:
                messagebox.showinfo("Info", "Operation cancelled. Webcam enable requires administrator privileges.")
                return
        
        try:
            # Try to run enable_cam.bat if it exists
            enable_script = os.path.join(self.base_dir, "enable_cam.bat")
            if os.path.exists(enable_script):
                # Run the batch file
                result = subprocess.run(
                    ["cmd", "/c", enable_script], 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    cwd=self.base_dir
                )
                
                if result.returncode == 0:
                    messagebox.showinfo(
                        "Webcam Enabled", 
                        "Webcam has been enabled successfully!\n\n"
                        "The webcam should now be enabled immediately.\n"
                        "Try opening the Camera app to test.\n\n"
                        "If the camera doesn't work:\n"
                        "• Close and reopen the camera app\n"
                        "• Try a different camera application\n"
                        "• Check Device Manager for camera status\n\n"
                        "The changes are now active without requiring a restart."
                    )
                    self.logger.log("Webcam enabled successfully")
                    # Log successful webcam enable to Firebase
                    self.firebase_manager.log_event(
                        "WEBCAM_ENABLED", 
                        "Webcam enabled successfully",
                        "INFO",
                        {"method": "batch_script", "return_code": result.returncode}
                    )
                else:
                    error_msg = result.stderr if result.stderr else "Unknown error occurred"
                    messagebox.showerror("Error", f"Failed to enable webcam.\n\nError: {error_msg}")
                    self.logger.log(f"Failed to enable webcam: {error_msg}")
                    # Log failed webcam enable to Firebase
                    self.firebase_manager.log_event(
                        "WEBCAM_ENABLE_FAILED", 
                        f"Failed to enable webcam: {error_msg}",
                        "ERROR",
                        {"method": "batch_script", "return_code": result.returncode, "error": error_msg}
                    )
            else:
                messagebox.showinfo("Info", "Enable script not found. Please ensure 'enable_cam.bat' is in the same directory as the application.")
                self.logger.log("Enable script not found")
        except Exception as e:
            print(f"Error enabling webcam: {e}")
            self.logger.log(f"Error enabling webcam: {e}")
            messagebox.showerror("Error", f"Failed to enable webcam: {e}")
    
    def show_logs_window(self):
        """Display logs in a new window"""
        logs_window = tk.Toplevel(self.root)
        logs_window.title("Application Logs")
        logs_window.geometry("600x400")
        logs_window.configure(bg="#000000")
        
        # Create text widget for logs
        logs_text = scrolledtext.ScrolledText(
            logs_window,
            bg="#000000",
            fg="#FFFFFF",
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        logs_text.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Load and display logs
        logs = self.logger.get_logs()
        logs_text.insert(tk.END, logs)
        logs_text.config(state=tk.DISABLED)
    
    def show_firebase_events_window(self):
        """Display Firebase events in a new window"""
        events_window = tk.Toplevel(self.root)
        events_window.title("Firebase Security Events")
        events_window.geometry("800x600")
        events_window.configure(bg="#000000")
        
        # Create main frame
        main_frame = tk.Frame(events_window, bg="#000000")
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg="#000000")
        status_frame.pack(fill="x", pady=(0, 10))
        
        # Firebase connection status
        status_text = "Connected" if self.firebase_manager.is_connected else "Disconnected"
        status_color = "#4CAF50" if self.firebase_manager.is_connected else "#FF4D4D"
        
        status_label = tk.Label(
            status_frame,
            text=f"Firebase Status: {status_text}",
            font=("Arial", 12, "bold"),
            fg=status_color,
            bg="#000000"
        )
        status_label.pack(side="left")
        
        # Refresh button
        refresh_btn = tk.Button(
            status_frame,
            text="Refresh",
            command=lambda: self.refresh_firebase_events(events_text),
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side="right")
        
        # Create text widget for events
        events_text = scrolledtext.ScrolledText(
            main_frame,
            bg="#000000",
            fg="#FFFFFF",
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        events_text.pack(expand=True, fill="both")
        
        # Load and display events
        self.load_firebase_events(events_text)
    
    def load_firebase_events(self, text_widget):
        """Load Firebase events into the text widget"""
        text_widget.delete(1.0, tk.END)
        
        if not self.firebase_manager.is_connected:
            text_widget.insert(tk.END, "Firebase is not connected. Please check your configuration.\n")
            return
        
        try:
            events = self.firebase_manager.get_recent_events(limit=100)
            
            if not events:
                text_widget.insert(tk.END, "No events found in Firebase database.\n")
                return
            
            text_widget.insert(tk.END, f"Found {len(events)} recent security events:\n\n")
            
            for event in events:
                # Format timestamp
                timestamp = event.get('timestamp', 'Unknown')
                if hasattr(timestamp, 'strftime'):
                    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    timestamp_str = str(timestamp)
                
                # Format event data
                event_type = event.get('event_type', 'Unknown')
                description = event.get('description', 'No description')
                severity = event.get('severity', 'INFO')
                
                # Color code based on severity
                severity_colors = {
                    'INFO': '#4CAF50',
                    'WARNING': '#FFA500',
                    'ERROR': '#FF4D4D',
                    'CRITICAL': '#FF0000'
                }
                
                color = severity_colors.get(severity, '#FFFFFF')
                
                # Insert event with formatting
                text_widget.insert(tk.END, f"[{timestamp_str}] ", "timestamp")
                text_widget.insert(tk.END, f"{event_type} ", "event_type")
                text_widget.insert(tk.END, f"({severity}): ", ("severity", severity))
                text_widget.insert(tk.END, f"{description}\n", "description")
                
                # Add additional data if available
                additional_data = event.get('additional_data', {})
                if additional_data:
                    text_widget.insert(tk.END, f"    Additional Data: {additional_data}\n", "additional")
                
                text_widget.insert(tk.END, "\n")
            
            # Configure tags for colors
            text_widget.tag_configure("timestamp", foreground="#888888")
            text_widget.tag_configure("event_type", foreground="#00BFFF")
            text_widget.tag_configure("severity", foreground="#FFA500")
            text_widget.tag_configure("description", foreground="#FFFFFF")
            text_widget.tag_configure("additional", foreground="#CCCCCC")
            
            # Configure severity-specific colors
            for severity, color in severity_colors.items():
                text_widget.tag_configure(severity, foreground=color)
                
        except Exception as e:
            text_widget.insert(tk.END, f"Error loading Firebase events: {e}\n")
    
    def refresh_firebase_events(self, text_widget):
        """Refresh Firebase events display"""
        self.load_firebase_events(text_widget)
    
    def show_status_window(self):
        """Display system status in a new window"""
        status_window = tk.Toplevel(self.root)
        status_window.title("System Status")
        status_window.geometry("500x400")
        status_window.configure(bg="#000000")
        
        # Create text widget for status
        status_text = scrolledtext.ScrolledText(
            status_window,
            bg="#000000",
            fg="#FFFFFF",
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        status_text.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Get and display status information
        status_info = []
        status_info.append("=== SYSTEM STATUS ===\n")
        
        # Webcam status
        webcam_status = self.system_checker.check_webcam_status()
        status_info.append(f"Webcam Status: {webcam_status}")
        
        # USB storage status
        usb_status = self.system_checker.check_usb_storage()
        status_info.append(f"USB Storage: {usb_status}")
        
        # System info
        system_info = self.system_checker.get_system_info()
        status_info.append("\n=== SYSTEM INFORMATION ===")
        for info in system_info:
            status_info.append(info)
        
        # Facial recognition info
        known_faces = self.face_recognition.get_known_faces()
        status_info.append("\n=== FACIAL RECOGNITION ===")
        if known_faces:
            status_info.append(f"Registered faces: {', '.join(known_faces)}")
        else:
            status_info.append("No faces registered")
        
        status_text.insert(tk.END, "\n".join(status_info))
        status_text.config(state=tk.DISABLED)
    
    def register_face(self):
        """Register a new face for recognition"""
        # Authenticate user (password or face recognition)
        if not self.authenticate_admin("register face"):
            return
        
        # Get name for the face
        name = simpledialog.askstring(
            "Register Face",
            "Enter name for the person to register:",
            show="*"
        )
        
        if not name:
            messagebox.showinfo("Info", "Face registration cancelled.")
            return
        
        # Check if name already exists
        known_faces = self.face_recognition.get_known_faces()
        if name in known_faces:
            response = messagebox.askyesno(
                "Face Already Exists",
                f"Face '{name}' is already registered. Do you want to replace it?"
            )
            if not response:
                return
            # Remove existing face
            self.face_recognition.remove_face(name)
        
        # Start face registration
        self.logger.log(f"Face registration started for: {name}")
        
        # Hide the main window temporarily
        self.root.withdraw()
        
        try:
            # Capture face image
            if self.face_recognition.capture_face_image(name):
                messagebox.showinfo("Success", f"Face registered successfully for {name}")
                self.logger.log(f"Face registered successfully for: {name}")
                
                # Log to Firebase
                self.firebase_manager.log_event(
                    "FACE_REGISTERED",
                    f"Face registered for {name}",
                    "INFO",
                    {"name": name}
                )
            else:
                messagebox.showerror("Error", "Failed to register face. Please try again.")
                self.logger.log(f"Face registration failed for: {name}")
        except Exception as e:
            messagebox.showerror("Error", f"Error during face registration: {e}")
            self.logger.log(f"Face registration error: {e}")
        finally:
            # Show the main window again
            self.root.deiconify()
    
    def test_face_recognition(self):
        """Test facial recognition in real-time"""
        # Authenticate user (password or face recognition)
        if not self.authenticate_admin("test face recognition"):
            return
        
        # Check if any faces are registered
        known_faces = self.face_recognition.get_known_faces()
        if not known_faces:
            messagebox.showinfo("Info", "No faces registered. Please register faces first.")
            return
        
        self.logger.log("Face recognition test started")
        
        # Hide the main window temporarily
        self.root.withdraw()
        
        try:
            # Start recognition test
            self.face_recognition.test_recognition()
            self.logger.log("Face recognition test completed")
        except Exception as e:
            messagebox.showerror("Error", f"Error during recognition test: {e}")
            self.logger.log(f"Face recognition test error: {e}")
        finally:
            # Show the main window again
            self.root.deiconify()
    
    def delete_face(self):
        """Delete a registered face"""
        # Authenticate user (password or face recognition)
        if not self.authenticate_admin("delete face"):
            return
        
        # Get list of registered faces
        known_faces = self.face_recognition.get_known_faces()
        if not known_faces:
            messagebox.showinfo("Info", "No faces registered to delete.")
            return
        
        # Create a simple dialog to select face to delete
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Registered Face")
        delete_window.geometry("400x300")
        delete_window.configure(bg="#000000")
        delete_window.transient(self.root)
        delete_window.grab_set()
        
        # Center the window
        delete_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Main frame
        main_frame = tk.Frame(delete_window, bg="#000000")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Select Face to Delete",
            font=("Arial", 16, "bold"),
            fg="#FFFFFF",
            bg="#000000"
        )
        title_label.pack(pady=(0, 20))
        
        # Listbox for faces
        listbox_frame = tk.Frame(main_frame, bg="#000000")
        listbox_frame.pack(expand=True, fill="both", pady=(0, 20))
        
        listbox = tk.Listbox(
            listbox_frame,
            bg="#333333",
            fg="#FFFFFF",
            font=("Arial", 12),
            selectmode=tk.SINGLE,
            height=8
        )
        listbox.pack(expand=True, fill="both")
        
        # Populate listbox
        for face in known_faces:
            listbox.insert(tk.END, face)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#000000")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a face to delete.")
                return
            
            selected_face = listbox.get(selection[0])
            
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete the face registration for '{selected_face}'?\n\nThis action cannot be undone."
            )
            
            if confirm:
                if self.face_recognition.remove_face(selected_face):
                    messagebox.showinfo("Success", f"Face registration for '{selected_face}' has been deleted.")
                    self.logger.log(f"Face registration deleted for: {selected_face}")
                    
                    # Log to Firebase
                    self.firebase_manager.log_event(
                        "FACE_DELETED",
                        f"Face registration deleted for {selected_face}",
                        "INFO",
                        {"name": selected_face}
                    )
                    
                    # Close window and refresh list
                    delete_window.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to delete face registration for '{selected_face}'.")
        
        def cancel():
            delete_window.destroy()
        
        # Delete button
        btn_delete = tk.Button(
            buttons_frame,
            text="Delete Selected",
            command=delete_selected,
            font=("Arial", 12, "bold"),
            bg="#FF5722",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10
        )
        btn_delete.pack(side="left", padx=(0, 10))
        
        # Cancel button
        btn_cancel = tk.Button(
            buttons_frame,
            text="Cancel",
            command=cancel,
            font=("Arial", 12, "bold"),
            bg="#666666",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10
        )
        btn_cancel.pack(side="right")
        
        # Focus on listbox
        listbox.focus_set()
        
        # Bind double-click to delete
        listbox.bind('<Double-Button-1>', lambda e: delete_selected())
        
        # Wait for window to close
        delete_window.wait_window()
    
    def authenticate_admin(self, action_name):
        """Authenticate admin using password or face recognition"""
        # Check if any faces are registered
        known_faces = self.face_recognition.get_known_faces()
        has_registered_faces = len(known_faces) > 0
        
        # Create authentication choice dialog
        auth_window = tk.Toplevel(self.root)
        auth_window.title("Admin Authentication")
        auth_window.geometry("400x250")
        auth_window.configure(bg="#000000")
        auth_window.transient(self.root)
        auth_window.grab_set()
        
        # Center the window
        auth_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Main frame
        main_frame = tk.Frame(auth_window, bg="#000000")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text=f"Authentication Required",
            font=("Arial", 16, "bold"),
            fg="#FFFFFF",
            bg="#000000"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text=f"To {action_name}",
            font=("Arial", 12),
            fg="#CCCCCC",
            bg="#000000"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#000000")
        buttons_frame.pack(expand=True, fill="both", pady=(20, 0))
        
        auth_result = {"success": False, "method": None}
        
        def password_auth():
            auth_window.destroy()
            admin_password = simpledialog.askstring(
                "Admin Authentication",
                "Enter admin password:",
                show="*"
            )
            if admin_password == self.current_admin_password:
                auth_result["success"] = True
                auth_result["method"] = "password"
                self.logger.log(f"Successful authentication via password for: {action_name}")
            else:
                messagebox.showerror("Error", "Incorrect admin password.")
                self.logger.log(f"Failed authentication via password for: {action_name}")
        
        def face_auth():
            if not has_registered_faces:
                messagebox.showinfo("Info", "No faces registered. Please register faces first.")
                return
            
            auth_window.destroy()
            
            # Hide main window temporarily
            self.root.withdraw()
            
            try:
                # Start face recognition for authentication
                if self.authenticate_with_face():
                    auth_result["success"] = True
                    auth_result["method"] = "face"
                    self.logger.log(f"Successful authentication via face recognition for: {action_name}")
                    
                    # Log to Firebase
                    self.firebase_manager.log_event(
                        "FACE_AUTH_SUCCESS",
                        f"Face authentication successful for {action_name}",
                        "INFO",
                        {"action": action_name}
                    )
                else:
                    messagebox.showerror("Error", "Face authentication failed.")
                    self.logger.log(f"Failed authentication via face recognition for: {action_name}")
                    
                    # Log to Firebase
                    self.firebase_manager.log_event(
                        "FACE_AUTH_FAILED",
                        f"Face authentication failed for {action_name}",
                        "WARNING",
                        {"action": action_name}
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Face authentication error: {e}")
                self.logger.log(f"Face authentication error for {action_name}: {e}")
            finally:
                # Show main window again
                self.root.deiconify()
        
        def cancel_auth():
            auth_window.destroy()
        
        # Password authentication button
        btn_password = tk.Button(
            buttons_frame,
            text="Use Password",
            command=password_auth,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_password.pack(pady=(0, 10), fill="x")
        
        # Face recognition button (only if faces are registered)
        if has_registered_faces:
            btn_face = tk.Button(
                buttons_frame,
                text="Use Face Recognition",
                command=face_auth,
                font=("Arial", 12, "bold"),
                bg="#2196F3",
                fg="#FFFFFF",
                relief=tk.FLAT,
                bd=0,
                padx=30,
                pady=15
            )
            btn_face.pack(pady=(0, 10), fill="x")
        else:
            # Show disabled button if no faces registered
            btn_face_disabled = tk.Button(
                buttons_frame,
                text="Use Face Recognition (No faces registered)",
                command=lambda: messagebox.showinfo("Info", "No faces registered. Please register faces first."),
                font=("Arial", 12, "bold"),
                bg="#666666",
                fg="#CCCCCC",
                relief=tk.FLAT,
                bd=0,
                padx=30,
                pady=15,
                state=tk.DISABLED
            )
            btn_face_disabled.pack(pady=(0, 10), fill="x")
        
        # Cancel button
        btn_cancel = tk.Button(
            buttons_frame,
            text="Cancel",
            command=cancel_auth,
            font=("Arial", 12, "bold"),
            bg="#666666",
            fg="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15
        )
        btn_cancel.pack(fill="x")
        
        # Wait for window to close
        auth_window.wait_window()
        
        return auth_result["success"]
    
    def authenticate_with_face(self, timeout=10):
        """Authenticate user using face recognition"""
        # Check if face detection is available
        if self.face_recognition.face_cascade is None:
            messagebox.showerror("Error", "Face detection is not available. Please ensure OpenCV is properly installed.")
            return False
            
        print("🔐 Starting face authentication...")
        print("Please look at the camera")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Could not open camera")
            return False
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        start_time = datetime.datetime.now()
        authenticated = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            # Recognize faces
            face_locations, face_names = self.face_recognition.recognize_faces(frame)
            
            # Draw results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw rectangle
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Draw name
                cv2.putText(frame, name, (left, top - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # Check if a known face is detected
                if name != "Unknown":
                    authenticated = True
                    break
            
            # Add info
            elapsed = (datetime.datetime.now() - start_time).seconds
            remaining = max(0, timeout - elapsed)
            
            cv2.putText(frame, f"Authentication: {remaining}s", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "Look at the camera", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to cancel", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Face Authentication', frame)
            
            # Check for timeout or key press
            if cv2.waitKey(1) & 0xFF == ord('q') or elapsed >= timeout:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if authenticated:
            print("✅ Face authentication successful!")
        else:
            print("❌ Face authentication failed")
        
        return authenticated
    
    def show_password_change_dialog(self):
        """Show dialog to change admin password"""
        # First ask for current password
        current_password = simpledialog.askstring(
            "Change Admin Password",
            "Enter current admin password:",
            show="*"
        )
        
        if current_password is None:  # User cancelled
            return
            
        if current_password != self.current_admin_password:
            messagebox.showerror("Error", "Current password is incorrect.")
            self.logger.log("Failed password change attempt - incorrect current password")
            return
        
        # Now ask for new password
        new_password = simpledialog.askstring(
            "Change Admin Password",
            "Enter new admin password:",
            show="*"
        )
        
        if new_password is None:  # User cancelled
            return
        
        if new_password:
            if len(new_password) >= 6:
                # In a real application, you'd want to hash this password
                # For now, we'll just store it in memory
                self.current_admin_password = new_password
                self.logger.log("Admin password changed successfully")
                messagebox.showinfo("Success", "Admin password has been changed successfully.")
            else:
                messagebox.showerror("Error", "Password must be at least 6 characters long.")
                self.logger.log("Failed password change attempt - password too short")
        else:
            messagebox.showerror("Error", "Password cannot be empty.")
            self.logger.log("Failed password change attempt - empty password")

# --- Supporting Classes ---
class Logger:
    def __init__(self):
        self.log_file = "app_log.txt"
        self.log_entries = []
    
    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.log_entries.append(log_entry)
        
        # Also write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")
        
        print(log_entry)
    
    def get_logs(self):
        return "\n".join(self.log_entries[-100:])  # Return last 100 entries

class SystemChecker:
    @staticmethod
    def check_webcam_status():
        """Check if webcam is enabled/disabled"""
        try:
            # Check registry for webcam status
            result = subprocess.run(
                ['reg', 'query', 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{6bdd1fc6-810f-11d0-bec7-08002be2092f}', '/v', 'UpperFilters'],
                capture_output=True, text=True, shell=True
            )
            if "ksthunk" in result.stdout:
                return "ENABLED"
            else:
                return "DISABLED"
        except:
            return "UNKNOWN"
    
    @staticmethod
    def check_usb_storage():
        """Check USB storage status"""
        try:
            result = subprocess.run(
                ['reg', 'query', 'HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR', '/v', 'Start'],
                capture_output=True, text=True, shell=True
            )
            if "0x3" in result.stdout:
                return "ENABLED"
            elif "0x4" in result.stdout:
                return "DISABLED"
            else:
                return "UNKNOWN"
        except:
            return "UNKNOWN"
    
    @staticmethod
    def get_system_info():
        """Get basic system information"""
        info = []
        try:
            # OS Info
            result = subprocess.run(['systeminfo'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "OS Name:" in line or "OS Version:" in line:
                        info.append(line.strip())
        except:
            info.append("System info unavailable")
        
        return info

def main():
    root = tk.Tk()
    app = WebcamSecurityInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main() 