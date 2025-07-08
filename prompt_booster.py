# prompt_booster_app.py

import gradio as gr
import requests

# Adjust this to match your Ollama server if different
OLLAMA_URL = "http://localhost:11434"

# You can edit this template to reflect your prompt logic
PROMPT_TEMPLATE = """
You are an expert proposal writer.

The user has written a simple or unclear prompt:
"{user_input}"

Your only task is to rewrite it into a brief, well-structured prompt for LLM. 

Do not include assumptions, generic statements, or content not grounded in the provided prompt.

No expansion, no additional context, just a clear and concise prompt.
"""


def boost_prompt(user_input):
    # Format the template
    formatted_prompt = PROMPT_TEMPLATE.format(user_input=user_input)

    # Call Ollama
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": "llama3.1:8b",  # You can change this model
                "messages": [
                    {"role": "user", "content": formatted_prompt}
                ],
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            return " Error: Failed to get response from Ollama."

        result = response.json()

        if "message" in result:
            return result["message"]["content"]
        elif "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"]
        else:
            return " Error: Unexpected response format."

    except Exception as e:
        return f" Exception occurred: {str(e)}"

# Gradio UI
with gr.Blocks(title="Prompt Booster for Proposals") as demo:
    gr.Markdown("### 🛠️ Natural Language to Structured Prompt Converter")
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(label="💬 Enter your raw or simple prompt here", lines=5, placeholder="e.g. Write about electrical design...")
            generate_button = gr.Button("🚀 Boost Prompt")
        with gr.Column():
            output = gr.Textbox(label="📄 Boosted Prompt", lines=20)

    generate_button.click(fn=boost_prompt, inputs=[user_input], outputs=[output])

# Run the app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)

