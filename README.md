# Offline PDF Question-Answering System Using LLaMA

A **FastAPI-based offline chatbot** that allows users to upload PDFs and ask questions based on their content. The system uses a **CPU-friendly LLaMA model** for natural language understanding and response generation, with a modern and responsive user interface.


## Project Overview
This project provides a local, offline solution for interacting with PDF documents using AI. Users can upload PDF files and ask natural language questions. The system extracts the text content and generates responses using a lightweight LLaMA model. It is designed to run entirely offline on CPU-based machines, making it suitable for environments with limited internet or GPU access.

---

## Features
- Upload PDF documents and extract text content.
- Ask questions based on the PDF content.
- Fully **offline**, no API keys required.
- CPU-friendly LLaMA 1B Instruct Q4_K_M model.
- Modern and responsive web UI with dark mode and glassmorphism style.

---

## Folder Structure
local-pdf-chatbot/
├── backend/
│ ├── main.py # FastAPI backend
│ └── models/
│ └── llama-3.2-1b-instruct-q4_k_m.gguf
└── frontend/
├── index.html # Web UI
└── style.css # CSS styling

Usage
Upload PDF

Click the Upload PDF button.

Select a PDF file from your computer.

Wait for confirmation that text extraction is complete.

Ask Questions

Type a question in the textarea.

Click Ask.

The answer will appear in the stylized answer box.
