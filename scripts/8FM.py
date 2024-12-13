#! /usr/bin/python3

import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url):
    try:
        response = s.get(url, timeout=15).text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return

    if '.m3u8' not in response:
        if windows:
            print('https://raw.githubusercontent.com/AqFad2811/video/main/harapmaaf/harapmaaf.m3u8')
            return
        
        # Download the content to a temporary file
        try:
            temp_response = requests.get(url, timeout=15)
            temp_response.raise_for_status()  # Raise an error for bad responses
            with open('temp.txt', 'w') as temp_file:
                temp_file.write(temp_response.text)
        except requests.RequestException as e:
            print(f"Error downloading URL {url}: {e}")
            return

        with open('temp.txt', 'r') as temp_file:
            response = temp_file.read()

        if '.m3u8' not in response:
            print('https://raw.githubusercontent.com/AqFad2811/video/main/harapmaaf/harapmaaf.m3u8')
            return

    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end-tuner:end]:
            link = response[end-tuner:end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5

    streams = s.get(link[start:end]).text.split('#EXT')
    hd = streams[-1].strip()
    st = hd.find('http')
    print(hd[st:].strip())

print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')

s = requests.Session()
with open('../8fm_info.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
        else:
            grab(line)

# Clean up the temporary file if it exists
if os.path.exists('temp.txt'):
    os.remove('temp.txt')
