import base64

import openai
from flask import Blueprint, jsonify, request, send_from_directory
from fpdf import FPDF
import os
import openai
import fitz  # PyMuPDF

# Creating a blueprint for authentication
contract = Blueprint('contract', __name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
PDF_DIR = "generated_pdfs"

@contract.route('/gpt_highlight', methods=['POST'])
def gpt_highlight_helper():
    """API route for GPT-4o explanations"""
    data = request.json
    highlighted_text = data.get("text", "").strip()
    user_question = data.get("question", "What does this mean?").strip()

    if not highlighted_text:
        return jsonify({"error": "No highlighted text provided"}), 400

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains text. User's are trying to get clarity on certain sections of documents they are signing"},
                {"role": "user", "content": f"Explain this: '{highlighted_text}'. Question: {user_question}. Explain it short and casually like your telling a college student. Don't use formatting like bold, etc... Also if I ask about GTAWYB Tech Services Ltd then explain that you got the info from https://find-and-update.company-information.service.gov.uk/company/14820577. The registewd office address is 86-90 Paul Street, London, England, EC2A 4NE. The company status is Active. It was incorporated on 22 April 2023. Include the link I gave you when talking about GTAWYB Tech Services Ltd. NEVER include GTAWYB information if i ask to explain RSU's"}
            ]
        )

        ai_response = completion.choices[0].message.content

        return jsonify({"explanation": ai_response}), 200

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return jsonify({"error": "⚠️ AI failed to generate a response. Please try again."}), 500

@contract.route('/generate_contract', methods=['POST'])
def create_contract():
    data = request.json
    user_input = data.get("text", "")

    if not user_input:
        return jsonify({"error": "No contract details provided"}), 400

    try:
        # Generate contract using GPT-4o
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI contract generator."},
                {"role": "user", "content": f"Generate a contract for: {user_input}. No formatting like bold, etc...Alter the contract to include bracketed fill ins with the structure [LLC Name], [Company Type], [Office Address], [Company Number]. Do not have Cure Period included."}
            ]
        )

        contract_text = response.choices[0].message.content

        return jsonify({"contract": contract_text})

    except Exception as e:
        print(f"Error generating contract: {e}")
        return jsonify({"error": "Failed to generate contract"}), 500

@contract.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    contract_text = data.get("contract", "").strip()

    if not contract_text:
        return jsonify({"error": "No contract provided"}), 400

    # Ensure the directory exists
    PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_pdfs")
    os.makedirs(PDF_DIR, exist_ok=True)  # ✅ Ensure folder exists

    # Create a PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add contract text to PDF
    pdf.multi_cell(0, 10, contract_text)

    # Save the PDF
    pdf_filename = "contract.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)
    pdf.output(pdf_path)

    return jsonify({"pdf_url": f"generated_pdfs/{pdf_filename}"}), 200


@contract.route('/generated_pdfs/<filename>')
def serve_pdf(filename):
    PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_pdfs")
    return send_from_directory(PDF_DIR, filename)

@contract.route('/extract_text', methods=['POST'])
def extract_text_from_pdf():
    """API route to extract text from a full PDF file."""
    data = request.json
    pdf_base64 = data.get("pdfFile")

    if not pdf_base64:
        return jsonify({"error": "No PDF file provided"}), 400

    try:
        # Decode the base64-encoded PDF and write it to a temporary file
        pdf_data = pdf_base64.split(',')[1]  # Remove the "data:application/pdf;base64," prefix
        pdf_bytes = base64.b64decode(pdf_data)  # Decode the base64 string

        pdf_path = "temp_uploaded.pdf"
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        # Extract text from the PDF
        full_text = extract_text(pdf_path)

        # Clean up the temporary file
        os.remove(pdf_path)

        return jsonify({"fullText": full_text}), 200

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return jsonify({"error": "Failed to extract text from the PDF"}), 500

def extract_text(pdf_path):
    """Helper function to extract text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

@contract.route('/analyze_contract', methods=['POST'])
def analyze_contract():
    """API route to analyze the extracted contract text for missing clauses."""
    data = request.json
    full_text = data.get("fullText", "").strip()
    signer_situation = data.get("signerSituation", "").strip()

    if not full_text:
        return jsonify({"error": "No contract text provided"}), 400

    if not signer_situation:
        return jsonify({"error": "No signer situation provided"}), 400

    try:
        # Analyze the contract with GPT-4o
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a legal assistant specializing in analyzing contracts. Help identify any missing clauses based on the provided situation."},
                {"role": "user", "content": f"This is the contract: {full_text}\n\nBased on the situation: {signer_situation}, are there any important clauses missing? If so, list them and explain why they are needed in plain language. No formatting bold, etc... Label the missing clauses with numbers."},
            ]
        )

        ai_analysis = response.choices[0].message.content

        return jsonify({"analysis": ai_analysis}), 200

    except Exception as e:
        print(f"Error analyzing contract: {e}")
        return jsonify({"error": "Failed to analyze the contract"}), 500

@contract.route('/autofill', methods=['POST'])
def autofill_contract_with_gpt():
    """API route to use GPT to autofill a contract with provided data."""
    data = request.json
    contract_text = data.get("contractText", "").strip()
    autofill_data = data.get("autofillData", {})

    if not contract_text:
        return jsonify({"error": "No contract text provided"}), 400

    if not autofill_data:
        return jsonify({"error": "No autofill data provided"}), 400

    try:
        # Convert autofill data into a readable format for the prompt
        autofill_instructions = "\n".join([f"{key}: {value}" for key, value in autofill_data.items()])

        # Generate the GPT prompt
        gpt_prompt = f"""
        This is a contract template with placeholders such as [LLC Name], [Company Type], [Office Address], and [Company Number].
        Replace these placeholders with the provided data below:

        {autofill_instructions}

        Here is the contract template:
        {contract_text}
        
        Return the fully filled contract with all placeholders replaced by the correct data. No extra sentences. Only output the contract.
        
        The [LLC Name], [Company Type], [Office Address], and [Company Number] are for the client. The client is in the UK.
        
        Autofill my companies details where relevant too. My company is called Brighterway. My company address is 655 Gough St, San Francisco, CA 94102. My name is Walker Wells. Today's date is 02/10/2025.
        
        Do not output in markdown. No bold or other formatting... Remove Title from the contract. Add signature slot instead of "By" field. The ending should of the contract should have no exhibits. Make sure the two signatures spots at the bottom have my company Brighterway with my name Walker Wells filled in and a blank signature spot. The spots below should be identical with PRAGMATISM LABS LTD. as the company name and the Name and Date field empty.
        """

        # Use GPT to autofill the contract
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that autofills contract templates."},
                {"role": "user", "content": gpt_prompt}
            ]
        )

        filled_contract = response.choices[0].message.content.strip()

        return jsonify({"filledContract": filled_contract}), 200

    except Exception as e:
        print(f"Error autofilling contract with GPT: {e}")
        return jsonify({"error": "Failed to autofill the contract"}), 500
