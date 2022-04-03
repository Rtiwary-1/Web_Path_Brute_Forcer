#!/usr/bin/env python3

#######################################################################################
# -------------------------------------------------------------
# By: Raghavendra Tiwary, raghavendra.tiwary2002@gmail.com
# For: CLOUDSEK Backend Internship Program
# -------------------------------------------------------------

# ---------------------------------------------------------------------------
# TASK: Build a minimal web path brute-forcer: Optimized memory, CPU usage
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# This implementation is the first type of implementation.
# It is done using multithreading and for single url input.

# It has 3 inputs; all are required.
# First input is url; second input is the wordlist file; last input is the comma seperated or list input of success codes
# The sample success codes are : 200, 204, 301, 302, 307, 401, 403
# --------------------------------------------------------------------------------------------------------------------------


import requests
import argparse
import urllib.parse
import urllib3
import threading
import queue
import sys
import time


def parse_args():
    parser = argparse.ArgumentParser(description = "Brute force web directories; As a task for Cloudsek: ")
    parser.add_argument('-u', '--url', dest = 'url', help = 'URL to scan.', required = True)
    parser.add_argument('-w', '--wordlist', dest = 'wordlist', help = 'wordlist location; one word for each line', required = True)
    parser.add_argument('-s','--success_codes', dest = 'success_codes', default = 200, help = 'List of success codes as comma seperated input. Example: -s 200,302. Or as list: Example: [200,302]')
    parser.add_argument('-p', '--proxy', dest = 'proxy', default = None, help = 'send identified resources to this proxy. The proxy must do HTTP and HTTPS.')
    
    parser.add_argument('-t', '--threads', dest = 'threads', type = int, default = 10)
    return parser.parse_args()


def check_url(url,word_queue, args):
    while not word_queue.empty():
        try:
            # fetch a new word from the queue
            word = word_queue.get_nowait()
        except queue.Empty:
            # finish if the queue is empty
            break
        url = url + word.lstrip('/')
        if not url.endswith('/'):
            url += '/'
        response = requests.get(url, verify=False)
        input_status_code = args.success_codes
        length_status_code = len(args.success_codes)
        status_code = ""
        if (input_status_code[0] == "[" and input_status_code[-1] == "]"):
            c = args.success_codes[1:length_status_code-1].split(",")
            status_code = [int(x) for x in c]
        elif (input_status_code[0] == "[" and "]" not in input_status_code[-1]) or (input_status_code[-1] == "]" and "[" not in input_status_code):
            print("Invalid argument!")
            sys.exit(1)
        else:
            c = args.success_codes.split(",")
            status_code = [int(x) for x in c]
        if response.status_code in status_code:
            print(f'{url} [Status Code {response.status_code}]')  #({len(response.text)})
            if args.proxy is not None:
                proxies = {'http': args.proxy, 'https': args.proxy}
                requests.get(url, verify=False, proxies=proxies)


def main():
    
    args = parse_args()
    list_url = args.url
    n = len(list_url)
    list_url_final = []
    if (list_url[0] == "[" and list_url[-1] == "]"):
        list_url_final = args.url[1:n-1].split(",")
    elif (list_url[0] == "[" and "]" not in list_url[-1]) or (list_url[-1] == "]" and "[" not in list_url):
        print("Invalid argument!")
        sys.exit(1)
    else:
        list_url_final = args.url.split(",")

    

    # read wordlist and write each line into the queue
    words = open(args.wordlist).readlines()
    word_queue = queue.Queue()
    for word in words:
        word_queue.put(urllib.parse.quote(word.strip()))

    for i in list_url_final:
        if not i.endswith('/'):
            args.url = args.url + '/'

        threads = []
        for i in range(args.threads):
            t = threading.Thread(target=check_url, args=(i,word_queue, args))
            t.start()
            threads.append(t)


    

    while True:
        # the loop checks if the queue is empty and if all threads are dead. If so, the program exits
        try:
            time.sleep(0.5)
            if word_queue.empty() and True not in [t.is_alive() for t in threads]:
                sys.exit(0)
        except KeyboardInterrupt:
            while not word_queue.empty():
                try:
                    word_queue.get(block=False)
                except queue.Empty:
                    pass
            sys.exit(0)


if __name__ == "__main__":
    
    urllib3.disable_warnings()
    main()
    
