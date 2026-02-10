import os
import sys
import threading
import customtkinter as ctk
from PIL import Image
import numpy as np

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # window
        self.title("NeuralCare-Image")
        self.geometry(f"{1000}x{600}")
        self.resizable(False, False)

        # Main layout
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main Content (Results)
        self.grid_columnconfigure(2, weight=10) # Sub Content (Image)
        self.grid_rowconfigure(0, weight=1)

        # sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Sidebar toggle button
        self.sidebar_button = ctk.CTkButton(self, text="×", width=30, height=30,  
                                            font=ctk.CTkFont(size=24, weight="bold"), 
                                            corner_radius=15, 
                                            command=self.toggle_sidebar)
        self.sidebar_button.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.sidebar_visible = True

        # self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="NeuralCare", font=ctk.CTkFont(size=20, weight="bold"))
        # self.logo_label.grid(row=0, column=0, padx=20, pady=(60, 10))
        
        # Empty space
        self.spacer_label = ctk.CTkLabel(self.sidebar_frame, text="", height=50) 
        self.spacer_label.grid(row=0, column=0)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                       command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # middle section
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=(25, 0), pady=10, sticky="nsew") 
        self.main_frame.grid_rowconfigure(0, weight=0) # Title 
        self.main_frame.grid_rowconfigure(1, weight=1) # Results
        self.main_frame.grid_rowconfigure(2, weight=0) # Disclaimer

        # Title
        self.title_label = ctk.CTkLabel(self.main_frame, text="NeuralCare-Image", font=ctk.CTkFont(size=36, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="ew", pady=(5, 10))

        # Results 
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color=("gray90", "gray16"))
        self.result_frame.grid(row=1, column=0, sticky="nsew")
        self.result_frame.grid_propagate(False) # fixed size

        
        self.result_label = ctk.CTkLabel(self.result_frame, text="Loading Model...", font=ctk.CTkFont(size=30, weight="bold"))
        self.result_label.pack(pady=(100, 10))

        self.result_info_label = ctk.CTkLabel(self.result_frame, text="Please wait...", font=ctk.CTkFont(size=14), wraplength=350)
        self.result_info_label.pack(pady=(0, 100))

        self.confidence_label = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.confidence_label.pack(pady=(0, 5))

        self.confidence_progressbar = ctk.CTkProgressBar(self.result_frame, height=10)
        
        # Disclaimer
        self.disclaimer_label = ctk.CTkLabel(self.main_frame, text="This application is intended for research and educational purposes only. It is not a substitute for professional medical diagnosis. Please consult a dermatologist for an accurate assessment.",
                                             font=ctk.CTkFont(size=14), text_color="red", wraplength=350)
        self.disclaimer_label.grid(row=2, column=0, sticky="ew", pady=(10, 15))


        # Right Section
        self.sub_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray17"))
        self.sub_frame.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="nsew")
        self.sub_frame.grid_rowconfigure(0, weight=1) # Image 
        self.sub_frame.grid_rowconfigure(1, weight=0) # Buttons 
        self.sub_frame.grid_columnconfigure(0, weight=1)
        self.sub_frame.grid_propagate(False) # fixed size

        # Image Preview
        self.image_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.image_label = ctk.CTkLabel(self.image_frame, text="No Image Selected", font=ctk.CTkFont(size=14))
        self.image_label.pack(expand=True, fill="both")


        # Controls
        self.control_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
        self.control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Select Image Button
        self.main_button_1 = ctk.CTkButton(self.control_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Select Image", command=self.upload_image)
        self.main_button_1.pack(side="top", fill="x", pady=(0, 10))

        # Remove Image Button
        self.remove_button = ctk.CTkButton(self.control_frame, fg_color="transparent", border_width=2, border_color="red", text_color="red", hover_color=("#ffdddd", "#550000"), text="Remove Image", command=self.remove_image)
        self.remove_button.pack(side="top", fill="x")
        
        self.model = None
        self.load_model()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
            self.sidebar_button.configure(text="=")
            # Hide sidebar
            self.grid_columnconfigure(0, weight=0)
            self.sidebar_visible = False
        else:
            # Show sidebar
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            self.sidebar_button.configure(text="×")
            self.grid_columnconfigure(0, weight=0) 
            self.sidebar_visible = True
            
            self.sidebar_button.lift()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def load_model(self):
        # Load model in background thread
        threading.Thread(target=self._load_model_thread, daemon=True).start()

    def _load_model_thread(self):
        try:
            import tensorflow as tf
            import os 
            self.tf = tf
            
            # Locate model relative to this script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, '..', 'model.h5')
            model_path = os.path.abspath(model_path)
            
            print(f"Loading model from: {model_path}")
            self.model = self.tf.keras.models.load_model(model_path)
            print("Model loaded successfully")
            
            print(f"Loading model from: {model_path}")
            self.model = self.tf.keras.models.load_model(model_path)
            print("Model loaded successfully")
            
            # Notify main thread
            self.after(0, self.on_model_loaded)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.after(0, lambda: self.result_label.configure(text="Model Error"))

    def on_model_loaded(self):
        self.result_label.configure(text="Ready to Analyze")
        self.result_info_label.configure(text="Please upload an image to start.")
        self.main_button_1.configure(state="normal")
        self.remove_button.configure(state="normal")

    def upload_image(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.display_image(file_path)
            
            # Prepare UI for analysis
            self.result_label.configure(text="Analyzing...", text_color=("black", "white"))
            self.result_info_label.configure(text="Processing image...")
            self.confidence_label.configure(text="")
            
            self.confidence_progressbar.pack(pady=(0, 40), padx=40, fill="x") 
            self.confidence_progressbar.set(0)
            self.confidence_progressbar.configure(progress_color="orange") 

            if self.model:
                threading.Thread(target=self.predict, args=(file_path,), daemon=True).start()
            else:
                 self.result_label.configure(text="Please waiting...")
                 self.result_info_label.configure(text="Model loading in background.")

    def remove_image(self):
        # Clear image and reset text
        self.image_label.configure(image="") 
        self.image_label.configure(text="No Image Selected")
        self.my_image = None

        # Reset Results Frame
        self.result_label.configure(text="Ready to Analyze", text_color=("black", "white"))
        self.result_info_label.configure(text="Please upload an image to start.")
        self.confidence_label.configure(text="")
        
        self.confidence_progressbar.pack_forget() 
        self.confidence_progressbar.set(0)
    
    def display_image(self, file_path):
        image = Image.open(file_path)
        
    def display_image(self, file_path):
        image = Image.open(file_path)
        
        # Refresh dimensions to ensure accuracy before resizing
        self.update_idletasks() 
        frame_width = self.image_frame.winfo_width()
        frame_height = self.image_frame.winfo_height()
        
        # Substract padding (20px) to determine available space
        available_width = frame_width - 20
        available_height = frame_height - 20
        
        # Fallback if window hasn't rendered yet or is too small
        if available_width < 50: available_width = 400
        if available_height < 50: available_height = 400
        
        # Get sizing ratio
        img_w, img_h = image.size
        
        width_ratio = available_width / img_w
        height_ratio = available_height / img_h
        
        # Resize to fit within bounds
        resize_ratio = min(width_ratio, height_ratio)
        
        # Scale down a bit more (60%) to leave breathing room
        resize_ratio *= 0.6
        
        new_w = int(img_w * resize_ratio)
        new_h = int(img_h * resize_ratio)

        # Update image label
        self.my_image = ctk.CTkImage(light_image=image, dark_image=image, size=(new_w, new_h))
        self.image_label.configure(image=self.my_image, text="")
 

    def predict(self, img_path):
        if not self.model or not self.tf:
            return

        try:
            # Use local TF import
            img = self.tf.keras.preprocessing.image.load_img(img_path, target_size=(200, 200))
            img_array = self.tf.keras.preprocessing.image.img_to_array(img)
            img_array = self.tf.expand_dims(img_array, axis=0)

            predictions = self.model.predict(img_array)
            class_names = ['Benign', 'Malignant'] 
            predicted_class = class_names[np.argmax(predictions[0])]
            confidence = np.max(predictions[0])

            # Back to main thread for UI updates
            self.after(0, self.update_result, predicted_class, confidence)
        except Exception as e:
            print(f"Prediction error: {e}")
            self.after(0, self.result_label.configure, {"text": "Error"})

    def update_result(self, predicted_class, confidence):
        self.confidence_progressbar.pack(pady=(0, 40), padx=40, fill="x") # Ensure it's shown
        self.confidence_progressbar.set(confidence)
        self.confidence_label.configure(text=f"Confidence: {confidence:.1%}")
        
        if predicted_class == 'Malignant':
             self.result_label.configure(text=f"{predicted_class}", text_color="red")
             self.confidence_progressbar.configure(progress_color="red")
             self.result_info_label.configure(text="High risk detected. Consult a dermatologist immediately.")
        else:
             self.result_label.configure(text=f"{predicted_class}", text_color="green")
             self.confidence_progressbar.configure(progress_color="green")
             self.result_info_label.configure(text="Low risk detected. Regular checkups are still recommended.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
