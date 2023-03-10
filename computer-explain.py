#!/usr/bin/env python
from threading import Thread
import requests
import os
import re
import yt_dlp
from chatgpt import Conversation

def main():
    vid1 = GetSub()
    text1 = vid1.get_text()
    question_dict = {}
    question_dict['brief_summary'] = 'Give me a brief summary of this video\n'
    #question_dict['answer_to_title'] = f'the title of this video is "{video_title}" what was that discovery?\n'
    chatgpt = AskChatGPT()
    query = question_dict['brief_summary'] + text1
    #summation = chatgpt.ask(query)
    #print(summation)
    #summation = vid1.ask(quesitons, text1)
    # list engines
    #engines = openapi.Engine.list()
    # print the first engine's id
    #print(engines.data[0].id)

class GetSub():
    def __init__(self):
        self.video_url = input("Enter video-url: ")
        self.videoname = input("Enter name for video: ")
        self.get_raw_sub()
        self.remove_non_speach()
        
    def get_text(self):
        return self.text

    def get_raw_sub(self):
        #thread = Thread(target=yt_dlp.main, args=(["--write-auto-sub", "--sub-langs=en.*", "--skip-download", self.video_url, "-o", self.videoname],))
        thread = Thread(target=yt_dlp.main, args=(["--write-auto-sub", "--skip-download", self.video_url, "-o", self.videoname],))
        thread.start()
        thread.join()
        if os.path.exists(self.videoname + '.en-orig.vtt'):
            self.file_name = self.videoname + '.en-orig.vtt'
        else:
            self.file_name = self.videoname + '.en.vtt'

    def remove_non_speach(self):
        pattern = re.compile(r'^.*(\d{2}:\d{2}:\d{2}\.\d{3}).*$')
        self.text = ''
        with open(self.file_name, 'r') as file:
            print(f'opening file for reading {self.file_name}')
            lines = file.readlines()
        with open(self.file_name, 'w') as file:
            last_line = ''
            for line in lines:
                if not pattern.match(line) and line != last_line and line != ' \n' and line != '\n':
                    #print(f'line: {repr(line)}\nvsus: {repr(last_line)}')
                    last_line = line
                    line_cleaned = line.rstrip()
                    line_cleaned = line.replace('\n', ' ')
                    file.write(line_cleaned)
                    self.text = self.text + line_cleaned
        return self.text

class AskChatGPT():
    def ask(self, query):
        converstation = Conversation(config_path='')
        for chunk in converstation.stream(query):
            print(chunk, end="")

class AskGPT3():
    def __init__(self, openapi_key):
        self.openapi_key = openapi_key

    def ask(self, question, text):
        question = question + '\n' + text
        r = requests.post('https://api.genesistranslation.com/v1/gtp3',
                json={"user_key": self.openapi_key,
                    "query": question
                    })
        data = r.json()
        print(data['result'])

if __name__ == '__main__':
    main()

#financial
"""
1. Give me a breif summary of the video
2. provide me as many bullet points as you can about the video
3. Does the speaker(s) make any forecasts
"""
#scientific
"""
1. Give me a beif summary
2. Does this contradict any main stream scientific thought?
3. Give me as many bullet points as you can about the video?
"""
