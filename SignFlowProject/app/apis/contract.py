import openai
from flask import Blueprint, jsonify, request, send_from_directory
from fpdf import FPDF
import os
import openai

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
                {"role": "user", "content": f"Explain this: '{highlighted_text}'. Question: {user_question}. Explain it short and casually like your telling a college student. Don't use formatting like bold, etc..."}
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
                {"role": "user", "content": f"Generate a contract for: {user_input}. No formatting like bold, etc..."}
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
