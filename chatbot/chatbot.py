import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent

# venv\Scripts\activate
# deactivate

load_dotenv()

API_URL = os.getenv("API_URL")

@tool
def get_all_courses() -> str:
    """Get all available courses from API."""
    response = requests.get(f"{API_URL}/courses")
    return response.text

@tool
def get_courses_detail(course_name : str) -> str:
    """Get details of a course by course name from API."""
    response = requests.get(f"{API_URL}/courses/{course_name}")

    if response.status_code == 404:
        return "Course Not Found"
    return response.text

tools = [get_all_courses,get_courses_detail]    


llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature = 0
)

agent = create_agent(
    model = llm,
    tools = tools,
    system_prompt="""
You are a helpful AI chatbot.

You can answer general questions normally using Gemini.

Use tools only when the user asks about course data, fees, duration, or available courses.

If the user says hello, hi, hy, thanks, or asks general questions, answer directly without using tools.

Examples:
User: hi
Answer: Hello! How can I help you?

User: What is Python?
Answer normally.

User: Show all courses
Use get_all_courses tool.

User: What is the fee of Python?
Use get_course_detail tool.
"""
)

print("Chatbot started. Type 'exit' to stop.")

while True:
    user_input = input("You: ")

    if not user_input.strip():
        print("Bot: Please type something.")
        continue

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye!")
        break

    try:
        course_keywords = ["course", "courses", "fee", "fees", "duration", "python course", "data science course"]

        if any(word in user_input.lower() for word in course_keywords):
            response = agent.invoke({
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            })

            bot_response = response["messages"][-1].content

            if isinstance(bot_response, list):
                print("Bot:", bot_response[0]["text"])
            else:
                print("Bot:", bot_response)

        else:
            response = llm.invoke(user_input)
            bot_response = response.content

            if isinstance(bot_response, list):
                print("Bot:", bot_response[0]["text"])
            else:
                print("Bot:", bot_response)

    except Exception as e:
        print("Bot: Sorry, something went wrong.")
        print("Error:", e)