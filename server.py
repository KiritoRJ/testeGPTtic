from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configuração da API do OpenAI
openai.api_key = os.getenv("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")  # Certifique-se de definir essa variável no Render

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "running", "message": "Servidor WhatsApp-GPT está ativo!"})

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    try:
        # Obtendo dados da mensagem do WhatsApp
        data = request.json
        sender = data.get("sender", "Usuário")  # Número ou nome do remetente
        message = data.get("message", "")  # Texto enviado pelo usuário

        if not message:
            return jsonify({"error": "Nenhuma mensagem recebida!"}), 400

        # Processando a mensagem com o GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Modelo usado (ou substitua por gpt-4)
            messages=[
                {"role": "system", "content": "Você é um assistente no WhatsApp."},
                {"role": "user", "content": message}
            ]
        )

        gpt_reply = response["choices"][0]["message"]["content"]

        # Retornando resposta simulada para o WhatsApp
        return jsonify({
            "reply_to": sender,
            "message": gpt_reply
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Para executar localmente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
