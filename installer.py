import sys
import PIL as pil
import pyttsx3 as tts
import sqlite3 as sql
def sqlinit():
    conn=sql.connect("test.db")

def main():
    engine=tts.init("espeak")
    engine.say("Welcome")
    engine.runAndWait()
    print("SQLlite version: "+sql.version)

if __name__ == '__main__':
    main()
