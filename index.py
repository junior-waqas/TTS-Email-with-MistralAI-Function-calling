import whisper
from email.message import EmailMessage
import ssl
import smtplib
import functools
from mistralai import Mistral
import json
# tts part
model = whisper.load_model("tiny")
result = model.transcribe("")  # put your voice note here
stt_result = result['text']

print(stt_result)
# defining function


def email_sender(sender, receiver, subject, body):

    sender_login_pass = ""  # send login pass goes here
    # creating instance of email
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        # loging in
        smtp.login(sender, sender_login_pass)
        smtp.sendmail(sender, receiver, em.as_string())
    print(f'Email was sent to : {receiver}')


# json schema for mistral ai
tools = [
    {
        'type': 'function',
        'function': {
            'name': "email_sender",
            'description': 'sends an email to a receiver',
            'parameters': {
                'type': 'object',
                'properties': {
                    'subject': {
                        'type': 'string',
                        'description': 'The subject of the email'
                    },
                    'body': {
                        'type': 'string',
                        'description': 'The body of the email'
                    }
                }
            }
        }
    }
]

# using partial function to create a new function and putting them in a dictionar
# names_to_functions[function_name](**function_params)
names_to_functions = {
    # make sure to put sender and receiver email address here
    'email_sender': functools.partial(email_sender, sender="", receiver="")
}


# model
api_key = ""  # put your api key here
model = "mistral-large-latest"  # "open-mistral-7b"
mistral_client = Mistral(api_key=api_key)

# query
messages = messages = [
    {"role": "user", "content": stt_result},
    {'role': 'system', 'content': '''
      Do not include any Sender names or any extra info
     '''}]


response = mistral_client.chat.complete(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice='auto',
    parallel_tool_calls=False,
)


# extracting the tools from the response
tool_call = response.choices[0].message.tool_calls[0]
function_name = tool_call.function.name
function_params = json.loads(tool_call.function.arguments)

# executing the functions we got from mistral
function_result = names_to_functions[function_name](**function_params)
