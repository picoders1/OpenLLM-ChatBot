from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face API details
HF_API_KEY = "hf_HuQOVXWmiwgfrtrygtht444jjj"
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()  # Get JSON data safely
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_input = data["message"]

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": user_input}
    )

    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json[0].get("generated_text", "No response generated")
        return jsonify({"response": generated_text})  
    else:
        return jsonify({"error": "Hugging Face API failed", "status": response.status_code}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Ensure Flask runs on all interfaces