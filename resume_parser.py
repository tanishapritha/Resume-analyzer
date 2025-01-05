import spacy
import pdfplumber
import docx

# Load the spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()  # Extract text from each page
    return text

def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file.
    """
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])  # Combine all paragraphs into a string
    return text

def parse_resume(file_path):
    """
    Parse a resume to extract details like name, education, skills, and experience.
    """
    # Extract text based on file format (PDF or DOCX)
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("File format not supported. Use PDF or DOCX.")

    # Process the text using spaCy
    doc = nlp(text)

    # Initialize a dictionary to store extracted entities
    entities = {"name": None, "education": [], "skills": [], "experience": []}

    # Try to extract the name from the document using NER (Person entities)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not entities["name"]:
            entities["name"] = ent.text  # Set name if it's not already set

    # Fallback: If no name was detected, use the first line from the resume text
    if not entities["name"]:
        lines = text.split("\n")
        entities["name"] = lines[0].strip() if lines else "Unknown"

    # Extract organization names (for education or job experience)
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Organization entities could represent education or companies
            entities["education"].append(ent.text)

    # Extract job experience (using WORK_OF_ART for positions, might need adjustment based on data)
    for ent in doc.ents:
        if ent.label_ == "WORK_OF_ART":  # This is often used for job titles
            entities["experience"].append(ent.text)

    # Extract skills (using noun tokens in the document)
    entities["skills"] = [token.text for token in doc if token.pos_ == "NOUN"]

    return entities
