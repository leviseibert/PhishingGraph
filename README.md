# PhishingGraph

PhishingGraph is a methodology of utilizing machine learnig chatbots (particularly ChatGPT) to analyze social engineering threats.  In particular, PhishingGraph addresses human weaknesses and points out red flags in the messages under analysis.

PhishingGraph was born of out Levi Seibert's Master's Thesis, and that document, along with a conference paper explaining the methodolgy, are currently in review.

This project contains three Proof-Of-Concept Applications, each of which utilize the ChatGPT API (you will need to get your own API key; see https://openai.com/product).  They follow the PhishingGraph methodology, which consists of analyizing the message and providing a approximate percent chance of the message being a phish (or vish, in the case of PhishingGraph-Audio).  The user then has the ability to converse with the chatbot in regards to the message at hand and are provided three suggested options to gain the most from the experience:
 - A. See detailed reasons for the analysi
 - B. Get tips on avoiding phishing
 - C. Answer a quiz question about phsihing

These tools prove how machine learning chatbots can be utilized in helping non-expert users make expert decisions in regard to evaluating phishing threats.

## PhishingGraph-Text
PhishingGraph-Text is the simpliest of the the POCs, as it only evalutes simple text documents.  To utilize this chatbotcopy the text of an email to a .txt file and save in the same directory as PhishingGraph-Text.py.  To execute the application, run "python PhishingGraph-Text.py" from the command line, followed by the name of the text file.

## PhishingGraph-Audio
PhishingGraph-Audio is quite similar to PhishingGraph-Text, with the major difference being it handles audio input (via AssemblyAI's API; see https://www.assemblyai.com/dashboard/signup).  The user will pass the audio as a command line argument when running the script, and the application will transcribe the message and make its evaluation.

## PhishingGraph-Email
PhishingGraph-Email is most similar to traditional phishing reporting tools that are often used in organizations to allow users to forward suspicious emails to trained experts who determine the validity of the email.  PhishingGraph-Email emulates this process, however, it does not rely upon any users to provide feedback; the analysis is automatic.  To use this application, one needs to create an email account, and fill in the pertitient values within the code, including the address, password, and IMAP server.