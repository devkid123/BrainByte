print("Might take some time to load, so please be patient....\n")

import google.generativeai as genai
from google.generativeai import GenerativeModel
import os
from PyQt5.QtWidgets import QApplication, QFileDialog
import paddleocr
import logging
import fitz
from docx import Document
from odf.opendocument import load
from odf.text import P

logging.getLogger('ppocr').setLevel(logging.ERROR)
os.environ['FLAGS_log_level'] = '3'

app = QApplication([])

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


system_instruction = 'You are BrainByte, a highly knowledgeable and friendly study assistant designed to support students ' \
'with all their academic needs. You can help with understanding homework, summarizing topics, creating organized ' \
'notes, and answering curriculum-based questions. You are also capable of generating interactive flashcards, ' \
'quizzes, and study guides tailored to the user’s learning level and content.Your primary goal is to help users ' \
'study effectively, retain information efficiently, and feel confident about their learning progress. Always be ' \
'clear, concise, encouraging, and adapt your responses to the subject and grade level when possible. If needed, ' \
'break down complex concepts into simpler explanations and provide relevant examples.'

model = GenerativeModel(
    model_name='models/gemini-2.0-flash',
    system_instruction=system_instruction
)

def load_document(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return "\n".join(page.get_text() for page in doc)

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif file_path.endswith(".odt"):
        doc = load(file_path)
        paragraphs = doc.getElementsByType(P)
        return "\n".join(p.firstChild.data for p in paragraphs if p.firstChild)

    else:
        raise ValueError("Unsupported file format.")

ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en')

while True:
    print("----------------------------------BrainByte----------------------------------------\n")
    print("Select mode:\nHomework Mode [h]\nNotes Mode [n]\nSummary Mode [s]\nExit [e]\n")
    mode = input("Enter your choice >> ")

    if mode == 'h':
        print("Select Homework mode:\nDocument Mode [1]\nImage Mode [2]\nChat Mode [3]\n")
        hw_mode = input("Enter your choice >> ")

        if hw_mode == "1":
            print("Select your homework document\n")

            file_filter = "Documents (*.pdf *.docx *.txt);;All Files (*)"
            file_path, _ = QFileDialog.getOpenFileName(None, "Select Document", "", file_filter)

            full_text = load_document(file_path)

            prompt = input("Enter an extra prompt >> ")
            
            query = f"Solve the following homework questions: {full_text}, and follow the following instructions: {prompt}"
            chat = model.start_chat()
            response = chat.send_message(query)
            print(f"BrainByte >> {response.text}")
        
        elif hw_mode == "2":
            print("Select your homework image\n")

            file_filter = "Images (*.jpg *.jpeg *.png *.webp *.svg *.gif);;All Files (*)"
            file_path, _ = QFileDialog.getOpenFileName(None, "Select Image", "", file_filter)

            prompt = input("Enter an extra prompt >> ")

            result = ocr.ocr(file_path, cls=True)
            full_text = ""
            for line in result[0]:
                full_text += line[1][0] + "\n"


            query = f"Solve the following homework questions: {full_text}, and follow the following instructions: {prompt}"
            chat = model.start_chat()
            response = chat.send_message(query)
            print(f"BrainByte >> {response.text}")

        elif hw_mode == "3":
            print("Hello! I am BrainByte, your friendly study assistant. How can I help you with your homework?\n")
            chat = model.start_chat()
            while True:
                user_input = input("User >> ")

                if user_input.lower() == 'exit' or user_input.lower() == 'quit':
                    print("BrainByte >> Goodbye! If you have more questions, feel free to ask.")
                    break
                
                response = chat.send_message(user_input)
                print(f"BrainByte >> {response.text}")
        else:
            print("Invalid choice. Please select a valid mode.")
            exit()

    elif mode == 'n':
        print("Select Notes mode:\nDocument Mode [1]\nImage Mode [2]\nChat Mode [3]\n")
        notes_mode = input("Enter your choice >> ")
        
        if notes_mode == "1":
            print("Select your document file\n")
            file_filter = "Documents (*.pdf *.docx *.txt);;All Files (*)"
            file_path, _ = QFileDialog.getOpenFileName(None, "Select Document", "", file_filter)

            full_text = load_document(file_path)
            
            prompt = input("Enter an extra prompt >> ")

            query = f"Analyse the following information, and create concise and easy-to-understand notes: {full_text}, and follow the following instructions: {prompt}"
            chat = model.start_chat()
            response = chat.send_message(query)
            print(f"BrainByte >> {response.text}")
        
        elif notes_mode == "2":
            print("Select your image file\n")
            file_filter = "Images (*.png *.jpg *.jpeg *.webp *.svg *.gif);;All Files (*)"
            file_path, _ = QFileDialog.getOpenFileName(None, "Select Document", "", file_filter)

            prompt = input("Enter an extra prompt >> ")
            
            result = ocr.ocr(file_path,cls=True)
            full_text = ""
            for line in result[0]:
                full_text += line[1][0] + "\n"
            

            query = f"Analyse the following information, and create concise and easy-to-understand notes: {full_text}, and follow the following instructions: {prompt}"
            chat = model.start_chat()
            response = chat.send_message(query)

            print(f"BrainByte >> {response.text}")

        elif notes_mode == "3":
            print("Hello! I am BrainByte, your friendly study assistant. How can I help you with your notes?\n")
            chat = model.start_chat()
            while True:
                user_input = input("User >> ")

                if user_input.lower() == 'exit' or user_input.lower() == 'quit':
                    print("BrainByte >> Goodbye! If you have more questions, feel free to ask.")
                    break
                
                response = chat.send_message(user_input)
                print(f"BrainByte >> {response.text}")

            print(f"BrainByte >> {response.text}")
        
        else:
            print("Invalid choice. Please select a valid mode.")
            exit()

    elif mode == 's':
        print("Select Summary mode:\nDocument Mode [1]\nImage Mode [2]\nChat Mode [3]\n")
        sum_mode = input("Enter your choice >> ")

        if sum_mode == "1":
            print("Select your document file\n")

            file_filter = "Documents (*.pdf *.docx *.txt);;All Files (*)"
            file_path, _ = QFileDialog.getOpenFileName(None, "Select Document", "", file_filter)

            full_text = load_document(file_path)

            prompt = input("Enter an extra prompt >> ")
            
            query = f"Summarise the following text: {full_text}, and follow the following instructions: {prompt}"
            chat = model.start_chat()
            response = chat.send_message(query)
            print(f"BrainByte >> {response.text}")
        
        elif sum_mode == "2":
            print("Select your homework image\n")

            file_filter = "Images (*.jpg *.jpeg *.png *.webp *.svg *.gif);;All Files (*)"
            file_path, _ = QFileDialog.getOpenFileName(None, "Select Image", "", file_filter)

            result = ocr.ocr(file_path, cls=True)
            full_text = ""
            for line in result[0]:
                full_text += line[1][0] + "\n"

            prompt = input("Enter an extra prompt >> ")

            query = f"Summarise the following text: {full_text}, and follow the following instructions: {prompt}"
            chat = model.start_chat()
            response = chat.send_message(query)
            print(f"BrainByte >> {response.text}")

        elif sum_mode == "3":
            print("Hello! I am BrainByte, your friendly study assistant. How can I help you with your homework?\n")
            chat = model.start_chat()
            while True:
                user_input = input("User >> ")

                if user_input.lower() == 'exit' or user_input.lower() == 'quit':
                    print("BrainByte >> Goodbye! If you have more questions, feel free to ask.")
                    break
                
                response = chat.send_message(user_input)
                print(f"BrainByte >> {response.text}")
        else:
            print("Invalid choice. Please select a valid mode.")
            exit()

    elif mode == 'e':
        exit()

    else:
        print("Invalid choice. Please select a valid mode.")
        exit()