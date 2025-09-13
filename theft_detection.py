import cv2
import time
import threading
import json
import smtplib
from datetime import datetime
from queue import Queue
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ultralytics import YOLO

class TheftDetector:
    def send_email_alert(self, detection):
        """Send email alert in background thread"""
        def email_worker():
            try:
                sender_email = ""
                sender_password = ""
                receiver_email = ""
                
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = "THEFT ALERT - Security System"
                
                body = f"""THEFT DETECTED!
                
Timestamp: {detection['timestamp']}
Frame: {detection['frame_number']}
Confidence: {detection['confidence']:.2f}
Location: {detection['bbox']}
                
Immediate action required!"""
                
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                server.quit()
                print("Email alert sent!")
            except Exception as e:
                print(f"Email failed: {e}")
        
        # Send email in background thread to avoid blocking
        email_thread = threading.Thread(target=email_worker, daemon=True)
        email_thread.start()
    

    def __init__(self, model_path):
        self.model = YOLO(model_path)
        # Optimize for CPU inference
        self.model.overrides['device'] = 'cpu'
        self.model.overrides['half'] = False  # Disable FP16 for CPU
        
        # Frame processing optimization
        self.frame_queue = Queue(maxsize=2)
        self.result_queue = Queue(maxsize=2)
        self.processing = True
        
        # Logging
        self.detections = []
        self.frame_number = 0
        self.last_alert_time = 0
        self.alert_cooldown = 30  # 30 seconds between alerts
        
    def preprocess_frame(self, frame):
        """Resize frame to 640x640 for model input"""
        return cv2.resize(frame, (640, 640))
    
    def inference_worker(self):
        """Background thread for model inference"""
        while self.processing:
            if not self.frame_queue.empty():
                frame_data = self.frame_queue.get()
                frame, frame_num = frame_data
                results = self.model(frame, conf=0.5, verbose=False)
                if not self.result_queue.full():
                    self.result_queue.put((frame, results, frame_num))
    
    def process_video(self, video_source=0):
        """Process video stream with optimizations"""
        cap = cv2.VideoCapture(video_source)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  
        
        fps_counter = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self.frame_number += 1
            processed_frame = self.preprocess_frame(frame)
            results = self.model(processed_frame, conf=0.5, verbose=False)
            
            display_frame = frame.copy()
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        
                        # Scale coordinates back to original frame size
                        h_orig, w_orig = frame.shape[:2]
                        x1 = int(x1 * w_orig / 640)
                        y1 = int(y1 * h_orig / 640)
                        x2 = int(x2 * w_orig / 640)
                        y2 = int(y2 * h_orig / 640)
                        
                        # Log detection
                        detection = {
                            "timestamp": datetime.now().isoformat(),
                            "frame_number": self.frame_number,
                            "class": "shoplifting" if cls == 1 else "normal",
                            "confidence": conf,
                            "bbox": [x1, y1, x2, y2]
                        }
                        self.detections.append(detection)
                        
                        # Send alert for theft detection (non-blocking)
                        if cls == 1 and conf > 0.5:
                            current_time = time.time()
                            if current_time - self.last_alert_time > self.alert_cooldown:
                                self.send_email_alert(detection)
                                self.last_alert_time = current_time
                        
                        color = (0, 0, 255) if cls == 1 else (0, 255, 0)
                        label = f"THEFT {conf:.2f}" if cls == 1 else f"NORMAL {conf:.2f}"
                        
                        cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(display_frame, label, (x1, y1-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # FPS calculation
            fps_counter += 1
            if fps_counter % 30 == 0:
                fps = 30 / (time.time() - start_time)
                print(f"FPS: {fps:.1f}")
                start_time = time.time()
            
            cv2.imshow('Theft Detection System', display_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.processing = False
        cap.release()
        cv2.destroyAllWindows()
        
        # Save detections to JSON
        with open('detections.json', 'w') as f:
            json.dump(self.detections, f, indent=2)
        print(f"Saved {len(self.detections)} detections to detections.json")

# Usage
if __name__ == "__main__":
    detector = TheftDetector(r'C:\Users\yashc\Downloads\nuebAIstic\Theft_Detection_e200_smallModel_FYP_Dataset\weights\best_int8_openvino_model')
    detector.process_video(r"C:\Users\yashc\Downloads\nuebAIstic\samples\input1.mp4")