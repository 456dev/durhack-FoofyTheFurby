import argparse
import json
import os
import pathlib
import pprint
import random
import time
from typing import Sequence

import dotenv
import google.cloud.texttospeech as tts
import openai
import pydantic
import pydub
import pydub.playback

dotenv.load_dotenv()

parser = argparse.ArgumentParser(
    prog='FurbyReviewer',
    description='Forces the Furby to watch you code.',
    epilog='God help us all.')

parser.add_argument("-f", "--filename", default="code.txt")
args = parser.parse_args()


def get_voiceline_string(comment_frequency: int, style: int, error_guess: int,
    comment_politeness: int):
    abnormal_code = not all([abs(factor - 100) <= 25 for factor in
                             [comment_frequency, style, error_guess,
                              comment_politeness]])
    comment_alignment = 0 if abs(comment_politeness - 100) <= 25 else (
        -1 if comment_politeness < 100 else 1)
    comment_alignment_is_positive = comment_alignment == 0
    comment_frequency_is_positive = abs(comment_frequency - 100) <= 25
    comment_matches = comment_alignment_is_positive == comment_frequency_is_positive

    return f"""
  <speak><prosody rate="110%" pitch="150%">
    This code is {"<break time='0.4s'/>interesting" if abnormal_code else "acceptable"}.
    Your comments are {"creepy" if comment_alignment == -1 else ("bad" if comment_alignment == -1 else "good")}, {"and" if comment_matches else "but"} there are {"just" if comment_frequency_is_positive else "not"} enough of them.
    
  </prosody></speak>
  """


def unique_languages_from_voices(voices: Sequence[tts.Voice]):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


def list_languages():
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="\n" if i % 5 == 4 else "")


def list_voices(language_code=None):
    client = tts.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = tts.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")


def text_to_wav(voice_name: str, text: str, file: pathlib.Path):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(ssml=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    with open(file, "wb") as out:
        out.write(response.audio_content)
    print(f'Generated speech saved to "{file.name}"')


def ensure_file_generated(comment_frequency: int, style: int, error_guess: int,
    comment_politeness: int, voice_name: str, force: bool = False):
    file_name = f"cf{comment_frequency}_st{style}_eg{error_guess}_cn{comment_politeness}_vc{voice_name}.wav"
    path = pathlib.Path("media/generated/" + file_name)
    text = get_voiceline_string(comment_frequency, style, error_guess,
                                comment_politeness)
    if force or not path.exists():
        text_to_wav(voice_name, text, path)
    return path


def play_and_modulate(comment_frequency: int, style: int, error_guess: int,
    comment_politeness: int, voice_name: str, force: bool = False):
    path = ensure_file_generated(comment_frequency, style, error_guess,
                                 comment_politeness, voice_name, force)
    audioseg = pydub.AudioSegment.from_wav(path)
    subsegments = audioseg[::100]
    new_subsegments = [(seg + random.randrange(-60, 20) / 10) for seg in
                       subsegments]
    full_modulated = sum(new_subsegments)
    pydub.playback.play(full_modulated)


class AiResponse(pydantic.BaseModel):
    comment_frequency_reason: str
    comment_frequency: int
    style_reason: str
    style: int
    error_guess_reason: str
    error_guess: int
    comment_politeness_reason: str
    comment_politeness: int


print("[>] furby.init()")
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
    print("furby.babble_nonsense()")
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

print("[>] Furby.Thinking(1)")
print(f"[*] loading File {args.filename}")
with open(args.filename, "r") as file:
    x = file.readlines()
    print("[*] Read Lines")
CODE_CONTENT = "".join(x)
print("[*] Assembled content")
# print(CODE_CONTENT)

print("[*] Calling OpenAI Api")
time_to_ai = time.time()
try:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": CODE_CONTENT}],
        temperature=0.2,
        request_timeout=120
    )
except openai.error.Timeout as e:
    on_error("OpenAi TIMEOUT")
except openai.error.ServiceUnavailableError as e:
    on_error("OpenAi Unavalible")

print(f"[*] Got Response in {time.time() - time_to_ai}")
response = completion['choices'][0]['message']['content']

print(response)

print("[*] parsing response as json")

response_infomation = json.loads(response)

print("[*] validating against expected model")
ai_response = AiResponse.model_validate(response_infomation)

play_and_modulate(ai_response.comment_frequency, ai_response.style,
                  ai_response.error_guess, ai_response.comment_politeness,
                  "en-GB-Neural2-A", True)

pprint.pprint(ai_response)

# Takes in scores from ai and makes furby act accordingly

Scores = [ai_response.comment_frequency, ai_response.style,
          ai_response.error_guess]
print(ai_response.comment_frequency_reason)
print(f"[I] Score of {ai_response.comment_frequency}")
print(ai_response.style_reason)
print(f"[I] Score of {ai_response.style}")
print(ai_response.error_guess_reason)
print(f"[I] Score of {ai_response.error_guess}")
print(ai_response.comment_politeness_reason)
print(f"[I] Score of {ai_response.comment_politeness}")
Upperbound = 75
Lowerbound = 25


def scream():
    audioseg = pydub.AudioSegment.from_wav(
        pathlib.Path("media/hwoooooooooaaaaaaaaaah.wav"))
    pydub.playback.play(audioseg)
    print("[>] Furby.Scream()")


if 2 * Lowerbound < ai_response.comment_politeness < 2 * Upperbound:  # sees if comments are bad mannered or creepy nice
    lowestValue = 100
    highestValue = 0
    for x in Scores:  # loops to find highest and lowest score
        if x < lowestValue:
            lowestValue = x
        if x > highestValue:
            highestValue = x
    print("[>] Furby.Idle()=False")
    if lowestValue > Upperbound or highestValue > 95:
        print("[>] Furby.Boogy(5sec)")
    elif lowestValue < Lowerbound:
        scream()
    else:
        print("[>] Furby.bundleNunsence(2)")
else:
    # runs if comments are creeply nice or bad manners
    print("[>] Furby.Idle()=false")
    scream()
print("[>] Furby.Idle=true")
