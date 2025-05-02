import openai
from openai.agents import AgentBuilder, Tool
from flask import Flask, request, render_template

openai.api_key = "your-api-key"

app = Flask(__name__)

# Create assistant with tool
assistant = AgentBuilder(
    name="Smart Assistant",
    instructions="You're a helpful assistant that can calculate, analyze, and reason with tools and memory.",
    model="gpt-4-turbo",
    tools=[Tool.builtin("code_interpreter")]
).save()

# Create a persistent thread (for memory)
thread = openai.beta.threads.create()

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )
        run = openai.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
