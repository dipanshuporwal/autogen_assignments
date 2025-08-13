import pdfplumber
from docx import Document


def parse_file(file_path):
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    return text


# def parse_multiple_resumes(folder_path):
#     results = []
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         if filename.endswith((".pdf", ".docx", ".txt")):
#             parsed = parse_resume(file_path)
#             results.append(parsed)
#     return results
