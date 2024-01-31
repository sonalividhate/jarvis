#
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import openai



engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)  # male/female(1)
activationword = 'jarvis'
#

# Configure the web browser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def ai(prompt):

    openai.api_key = "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"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text


def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()




def parseCommand():
    listener = sr.Recognizer()
    print("Listening for Command")

    with sr.Microphone() as source:
        listener.pause_threshold = 2

        input_speech = listener.listen(source)

    try:
        print("recognising speech........")
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')

    except Exception as exception:
        print('Jarvis did not quite catch that')
        speak('Jarvis did not quite catch that')
        print(exception)
        return 'None'
    return query

#


def search_wikipedia(query=' '):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No Wikipedia page found')
        return 'No result recieved'
    try:
        wikiPage = wikipedia.page(searchResults[0])

    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])

    print(wikiPage.title)
    
    wikiSummary = str(wikiPage.summary)

    return wikiSummary
#


# main code
if __name__ == '__main__':
    print('All Systems Nominal.....')
    speak('All systems Nominal')

    while True:
        # pass the cammand as a list
        query = parseCommand().lower().split()
  
        if query[0] == activationword:
            query.pop(0)

            if 'hello' in query:
                speak('Jarvis says Greetings, all')

         # Navigation
        if query[0] == 'go' and query[1] == 'to':
            speak('Opening.....')
            query = ' '.join(query[2:])
            webbrowser.get('chrome').open_new(query)

         # Wikipedia
        if query[0] == 'what' and query[1] == 'is':
            query = ' '.join(query[2:])
            print('Finding your solution in universal encyclopedia.......')
            speak('Finding your solution in universal encyclopedia')

            speak(search_wikipedia(query))

        # open ai
        if query[0] == 'open':
            query = ' '.join(query[1:])
            print("Open ai")
            print(ai(query))
            speak(ai(query))
            
