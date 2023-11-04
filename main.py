import os
import pprint

import openai
import dotenv
import json
import pydantic
import time

dotenv.load_dotenv()

class AiResponse(pydantic.BaseModel):
    comment_frequency_reason: str
    comment_frequency: int
    style_reason: str
    style: int
    error_guess_reason: str
    error_guess: int
    comment_politeness_reason: str
    comment_politeness: int

# TODO furby.init()
"""
furby methods
init
babble_nonsense
idle
scream
thinking
custom sounds
"""


def on_error(msg: str):
    # TODO furby.babble_nonsense()
    print(f"[!] Error: {msg}")
    raise NotImplementedError(msg)


openai.api_key = os.environ.get("OPENAI_KEY", None)
if openai.api_key is None:
    raise Exception("NEED OPENAI KEY")

SYSTEM_PROMPT = """
You are a code reviewer that reviews code.

you will rate the inputed code by

rating the following factors from 0 to 100:
 - How well commented it is: "comment_frequency"
 - The code's style and formatting: "style"
 - how likely the code is to error when ran 0 is will error, 100 is no error: "error_guess"

rating how polite the comments are from 0 to 200: "comment_politeness"
0 is the worst, 100 is polite, and 200 is too polite, so it sounds creepy, or they are trying too hard
specifically, you should consider:
 - their manners within the comments (using please and thank you)
 - whether they greeted you at the start
 - whether they said goodbye at the end
if they mention the word "furby" within a comment, choose either exactly 0 or 200 as the rating.


you will output your chosen ratings as json, using the above keys, and the values as integers.
additionally, you will have another entry, the key suffixed with "_reason", which contains a concise
human-readable reason for why you chose that value.

=== example 1 ===
user:
# Hello Code Reviewer, have a good day #
########################################

# gets the random function
import random

var_a = 1
# Please get a random number
random_var_b = random.randint(1,5)

if var_a = random_var_b:
  print(f"oh WOW! there was a 1 in 5 change of this happening. can you roll a nat 20 as well? {random.randint(1,20))}")
else:
  # This is where the user would feel sad
  # here is a cat to make them feel better
  # (= ФェФ=)
  print(f"Better luck next time, with your lame {random_var_b}")

assistant:
{
  "comment_frequency_reason":"There are comments on most lines. some more complex lines should be more commented, other comments are just padding",
  "comment_frequency": 80,
  "style_reason": "related lines are a little spread apart, the variable var_a is defined but used only once, everything is on separate lines",
  "style": 75,
  "error_guess_reason": "there is 1 equals sign in the if statement",
  "error_guess": 5,
  "comment_politeness_reason": "mostly polite, but starts being a little creepy with the cat",
  "comment_politeness": 102
}

=== example 2 ===
user:
# fuck you and your shitty fucking screaming thing
# i haven't slept in days thanks to you
# enjoy this mess

__import__("os").system("loginctl lock-session");x=open("tmp.txt","w");x.write(__import__("string").printable*500);x.close();


assistant:
{
  "comment_frequency_reason":"There are not enough comments, for what the code does",
  "comment_frequency": 4,
  "style_reason": "all code is on 1 line, which is bad for readability, and is purposefully obfuscated",
  "style": 2,
  "error_guess_reason": "the code should execute correctly",
  "error_guess": 95,
  "comment_politeness_reason": "all present comments are targeted attacks and swearing and sarcasm",
  "comment_politeness": 1
}
"""

# TODO change to cli input

print("[*] loading File")
with open("code.txt", "r") as file:
    x = file.readlines()
    print("[*] Read Lines")
CODE_CONTENT = "".join(x)
print("[*] Assembled content")
print(CODE_CONTENT)

print("[*] Calling OpenAI Api")
time_to_ai = time.time()
completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": CODE_CONTENT}])

print(f"[*] Got Response in {time.time() - time_to_ai}")
response = completion['choices'][0]['message']['content']

print(response)

print("[*] parsing response as json")

response_infomation = json.loads(response)

print("[*] validating against expected model")
ai_response = AiResponse.model_validate(response_infomation)





pprint.pprint(ai_response)




"""
Print(ai_responce.comment_frequency_reason)
Read "comment_frequency"
Print(ai_responce.style_reason)
Read  "style"
Print(ai_responce.error_guess_reason)
Read "error_guess"
Print(ai_responce.comment_politeness_reason)
Read "comment_politeness"/2
ai_responce.comment_frequency
ai_responce.comment_frequency
ai_responce.comment_frequency
"""

# on file change

# openai api with updated code?

# parse json response

# get furby action


# input:
# file (once per run)
# file (run on change)
# api

# processing
# output


# output supports:
# read furby hardware
# furby emulator
