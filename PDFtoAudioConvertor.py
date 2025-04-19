import PyPDF2
import pyttsx3
import tkinter as tk
from tkinter import filedialog, messagebox
import threading


class PDFToAudioConverter:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.is_speaking = False

    def pdf_to_text(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                return text
        except Exception as e:
            messagebox.showerror("Error", f"Error reading PDF: {e}")
            return ""

    def text_to_speech(self, text):
        """Convert text to speech and play it in background"""
        def speak():
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False

        threading.Thread(target=speak, daemon=True).start()

    def stop_speech(self):
        if self.is_speaking:
            self.engine.stop()


class GUI:
    def __init__(self, root):
        self.root = root
        self.converter = PDFToAudioConverter()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.root.title("PDF to Audio Converter")
        self.root.geometry("400x250")

        self.label = tk.Label(self.root, text="Select a PDF file to convert to audio", font=("Arial", 14))
        self.label.pack(pady=20)

        self.upload_button = tk.Button(self.root, text="Upload PDF", font=("Arial", 12), command=self.upload_pdf)
        self.upload_button.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", font=("Arial", 12), command=self.play_audio)
        self.play_button.pack(pady=5)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            text = self.converter.pdf_to_text(file_path)
            if text.strip():
                self.text = text
                messagebox.showinfo("Success", "PDF loaded. Ready to convert to audio.")
            else:
                messagebox.showwarning("Warning", "No text found in PDF.")

    def play_audio(self):
        """Play the audio from the loaded text"""
        if hasattr(self, 'text') and self.text.strip():
            self.converter.text_to_speech(self.text)
        else:
            messagebox.showwarning("Warning", "Please upload a PDF first.")

    def on_closing(self):
        """Clean exit on window close"""
        self.converter.stop_speech()
        self.root.destroy()


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
