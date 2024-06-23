from pydub import AudioSegment
from pydub.playback import play

def Play():
    song = AudioSegment.from_mp3("speech.mp3")
    #play(song)