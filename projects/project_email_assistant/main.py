import os

from dotenv import load_dotenv
from imap_tools import MailBox
from openai import OpenAI

load_dotenv()

email_account = os.getenv("EMAIL_ACCOUNT")
email_password = os.getenv("EMAIL_PASSWORD")

llama_client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="local_ollama"
)

system_prompt = """
You are a helpful assistant that give royal-role response to e-mails that I receive.
You must respond in email format.
"""

def user_email_received_prompt(email_text):
    user_prompt = f"""
        Here is the email that I received: \n {email_text}
    """
    return user_prompt

with MailBox("imap.gmail.com").login(email_account, email_password) as mailbox:
    
    # fetch returns all emails; reverse=True = most recent first
    for msg in mailbox.fetch(limit=1, reverse=True):
        text = msg.text

    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_email_received_prompt(email_text=text)}
    ]

    response = llama_client.chat.completions.create(
        model="llama3.2:3b",
        messages=message
    )

print(response.choices[0].message.content)