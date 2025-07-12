# prompt_booster_app.py

import gradio as gr
import requests

# Adjust this to match your Ollama server if different
OLLAMA_URL = "http://localhost:11434"
# LLM_MODEL = "llama3.1:70b-instruct-q2_K"  # You can change this to your preferred model
LLM_MODEL = "llama3.1:8b"

# You can edit this template to reflect your prompt logic
PROMPT_TEMPLATE = """
You are an expert prompt rewriter for large language models (LLMs).

The user has written a simple or unclear prompt:
"{user_input}"
Your only task is to rewrite it into a clearer, more specific, structured prompt suitable for high-quality LLM responses.

If the user input is a **question**, identify the user's underlying goal or objective, and convert it into a clearer, more specific, structured prompt suitable for high-quality LLM responses.

You may rephrase it as a directive with bullet points or keep it as a refined question, whichever best supports a high-quality response.

You must follow these rules strictly:

1. You can choose to lists bullet points that makes the prompt clear and actionable when the user input is long.

2. Do not include assumptions, generic statements, or content not grounded in the provided prompt. 

3. Do not include quote marks or brackets, only the content of the prompt itself.

4. No expansion, no additional context or explanation of what you did — return raw, copy-pasteable prompt text only.

5. Always return output in both English and Chinese.

Your output must be precise, minimal, and suitable for direct use in an LLM call.
"""


def boost_prompt(user_input):
    # Format the template
    formatted_prompt = PROMPT_TEMPLATE.format(user_input=user_input)

    # Call Ollama
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": LLM_MODEL,  # You can change this model
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

