#!/usr/bin/env python3

import re
import spotipy.util as util
import requests
import time
import argparse
from wcwidth import wcswidth

sleep_time = 1
output = '{progress} / {duration} | {artist} - {title}'
maxlen = 5
barlen = 16

parser = argparse.ArgumentParser()

#input user information
parser.add_argument(
    '-i',
    '--userinfo',
    type=str, 
    metavar='username,client id,client secret',
    dest='userinfo'
)
#option args
parser.add_argument(
    '-f',
    '--format',
    type=str,
    metavar='custom format',
    dest='custom_format'
)
parser.add_argument(
    '-l',
    '--length',
    type=int,
    metavar='length',
    dest='length'
)
parser.add_argument(
    '-b',
    '--barlen',
    type=int,
    metavar='bar length',
    dest='barlen'
)
args = parser.parse_args()

if args.custom_format is not None:
    output = args.custom_format
if args.length is not None:
    maxlen = args.length
if args.barlen is not None:
    barlen = args.barlen

username = args.userinfo.split(',')[0]
client_id = args.userinfo.split(',')[1]
client_secret = args.userinfo.split(',')[2]
#---------------------------------------

def mil_to_min(mil):
    sec = mil/1000
    min = int(sec/60)
    sec = int(sec%60)
    return str(min) + ':' + str(sec).zfill(2)

redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-playback-state, user-modify-playback-state'

token = util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
}

response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
try:
    #Get JSON list
    response_json = response.json()
    
    #Modules
    progress = mil_to_min(response_json['progress_ms'])
    duration = mil_to_min(response_json['item']['duration_ms'])
    time_left = mil_to_min(response_json['item']['duration_ms']-response_json['progress_ms'])
    title = response_json['item']['name']
    artist = str(response_json['item']['artists']).split(',')[3][10:-1]
    album = response_json['item']['album']['name']
    track_number = response_json['item']['track_number']
    disc_number = response_json['item']['disc_number']
    volume = response_json['device']['volume_percent']
    pointer_loc = int((response_json['progress_ms']/response_json['item']['duration_ms'])*(barlen-1))
    bar = '-'*pointer_loc + '|' + '-'*(barlen-1-pointer_loc)

    #Output
    output = output.format(progress=progress, duration=duration, artist=artist,title=title, album=album, track_number=track_number, volume=volume, disc_number=disc_number, bar=bar, time_left = time_left)
    if wcswidth(output) > maxlen:
        while wcswidth(output) > maxlen - 3:
            output = output[:-1]
        output += '...'
    if wcswidth(output) < maxlen:
        output = output + ' ' * max(0, (maxlen - wcswidth(output)))
    print(output)

except:
    output = output.replace('{progress}','0:00').replace('{duration}','0:00').replace('{bar}','-'*barlen).replace('{volume}','00')
    print(re.sub('{[a-z]*}','N/A',output))
time.sleep(sleep_time)
