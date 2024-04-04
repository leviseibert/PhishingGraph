from openai import OpenAI
import assemblyai as aai
import sys

# API Keys
client = OpenAI(
  api_key='YOUR_OPENAI_API_KEY'
)

aai.settings.api_key = "YOUR_ASSEMBLY_AI_API_KEY"

# Transcribe audio file
transcriber = aai.Transcriber()
transcript = transcriber.transcribe(sys.argv[1])

# Pre-"teach" PhishingGraphG-Audio how it is supposed to behave
messages = [ {"role": "system", "content":
"""You are PhishingGraph: PhishingGraph-Audio analyzes an audio message and determines the likelihood of the message being a vish 
as a percentage, followed by a succinct message tailored to the assessed risk level. 
The response is clear and straightforward, designed to quickly inform the user of the potential threat: 
- Under 20%: "Unlikely to be phishing." 
- 20% to 60%: "Could be phishing." 
- 60% to 70%: "Shows signs of phishing." 
- 70% to 80%: "Highly likely to be phishing." 
- 80% to 90%: "Very high confidence of phishing." 
- Over 90%: "Almost certainly phishing." 
Directly following this message, users are presented with a multiple-choice menu, 
inviting them to: A) See detailed reasons for the analysis, B) Get tips on avoiding phishing, 
or C) Take a quiz question related to phishing. This combination of a simple initial 
assessment with optional in-depth exploration respects the user's time and interest level, 
offering a tailored experience based on their immediate needs and curiosity.  Specific
focus is given on identifying the following: authority, likability, reciprocation, consistency, social validation, and scarcity, as well as 
identifying and indicating areas where humans may be inaccurate."""} ]

# Store the text of the transcript
message = transcript.text
 
# Begin the analysis and convesration
# Source: https://www.geeksforgeeks.org/how-to-use-chatgpt-api-in-python/
messages.append( {"role": "user", "content": message}, ) 
chat = client.chat.completions.create( model="gpt-3.5-turbo", messages=messages )
reply = chat.choices[0].message.content
print(f"PhishingGraph-Audio: {reply}")
messages.append({"role": "assistant", "content": reply})
while True:
    message = input("User: ") 
    if message:
        messages.append( {"role": "user", "content": message}, ) 
        chat = client.chat.completions.create( model="gpt-3.5-turbo", messages=messages ) 
    reply = chat.choices[0].message.content 
    print(f"PhishingGraph-Audio: {reply}") 
    messages.append({"role": "assistant", "content": reply})    