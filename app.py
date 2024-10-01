from flask import Flask, render_template, request
import webbrowser
import pyttsx3
import platform
import os
import yt_dlp
import wikipediaapi

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate

# Initialize Wikipedia API with a proper user agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='JarvisAssistant/1.0 (https://github.com/PranshulJain/jarvis-assistant)'  # Specify your user agent here
)

# Register Chrome as the browser
chrome_path = r'C:/Users/pc/AppData/Local/Google/Chrome/Application/chrome.exe'  # Update this path if necessary
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def greet_user(command):
    """Respond to common greetings."""
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if any(greet in command for greet in greetings):
        return "Hi sir, nice to meet you."
    return None

def shutdown_computer():
    """Shutdown the computer."""
    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")  # Shutdown immediately on Windows
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("sudo shutdown now")  # Shutdown on Linux or macOS
    return "Shutting down the computer."

def restart_computer():
    """Restart the computer."""
    if platform.system() == "Windows":
        os.system("shutdown /r /t 1")  # Restart immediately on Windows
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("sudo reboot")  # Restart on Linux or macOS
    return "Restarting the computer."

def open_website(website_name):
    """Open websites dynamically based on the input."""
    if website_name:
        url = f"https://www.{website_name}.com"
        webbrowser.get('chrome').open(url)
        return f"Opening {website_name}."
    else:
        return "Please specify the website to open."

def play_song(song_name):
    """Play a song based on the name using YouTube."""
    if song_name:
        search_query = '+'.join(song_name.split())
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
            'extract_flat': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            if 'entries' in info_dict:
                video_url = f"https://www.youtube.com/watch?v={info_dict['entries'][0]['id']}"
                webbrowser.get('chrome').open(video_url)
                return f"Playing {song_name}."
            else:
                return "Sorry, I couldn't find that song on YouTube."
    else:
        return "Please specify the name of the song."

def search_wikipedia(topic):
    """Search Wikipedia for the given topic."""
    try:
        page = wiki_wiki.page(topic)
        if page.exists():
            return f"Here is a summary for {topic}: {page.summary[:500]}..."  # Truncate the summary
        else:
            return f"Sorry, I couldn't find any specific results for '{topic}'. Please try a more specific query."
    except Exception as e:
        return f"An error occurred while searching Wikipedia: {str(e)}"

def get_creator():
    """Return the name of the creator."""
    creator_name = "My creator is Pranshul Jain."
    speak(creator_name)
    return creator_name

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        command = request.form['command'].lower()

        # Check for greetings
        greeting_response = greet_user(command)
        if greeting_response:
            result = greeting_response
        elif "shutdown" in command:
            result = shutdown_computer()
        elif "restart" in command:
            result = restart_computer()
        elif "open" in command:
            website_name = command.replace("open", "").strip()
            result = open_website(website_name)
        elif "play" in command:
            song_name = command.replace("play", "").strip()
            result = play_song(song_name)
        elif "search" in command:
            topic = command.replace("search", "").strip()
            result = search_wikipedia(topic)
        elif "who is your creator" in command:
            result = get_creator()
        else:
            result = "Sorry, I didn't understand that command."

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
