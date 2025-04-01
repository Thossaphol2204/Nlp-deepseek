from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Initialize the Flask app
app = Flask(__name__)

# Load the model and tokenizer

model_path = r"C:\Users\KATANA\OneDrive\เดสก์ท็อป\ProjectDeep\Fine tunned model"

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Function to generate chatbot responses
def generate_text(prompt, max_length=0):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model.generate(
                **inputs, 
                    max_length=50,  # ไม่ยาวเกินไป
                    temperature=0.8,  # สมดุลระหว่าง creativity & accuracy
                    top_p=0.9,       # ใช้ Nucleus Sampling กรองคำตอบคุณภาพ
                    repetition_penalty=1.3,
                    num_beams=3,     # Beam Search แบบพอประมาณ
                    early_stopping=True,
                    do_sample=True   # เปิดโอกาสให้มีความหลากลาย
                )
    return tokenizer.decode(output[0], skip_special_tokens=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if user_input:
        # Generate chatbot response
        response = generate_text(user_input)
        return jsonify({"response": response})
    return jsonify({"response": "Please enter a message."})

if __name__ == "__main__":
    app.run(debug=True)