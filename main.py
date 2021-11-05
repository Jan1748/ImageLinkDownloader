import os
import threading

import requests


def main():
    links = get_file_links()
    for link in links:
        download_link(link)


def main_threads(total_threads, beginning_line=0):
    links = get_file_links()
    threads = []
    for i in range(total_threads):
        threads.append(threading.Thread(target=thread_function, args=(links, i, total_threads, beginning_line)))
    for thread in threads:
        thread.start()


def thread_function(links, thread_nr, offset, beginning_line):
    total_links = len(links)
    for i in range(beginning_line + thread_nr, len(links), offset):
        t = ''
        if thread_nr < 10:
            t = '0'
        print(f'Thread nr {t}{thread_nr} is working on link ({i + 1} / {total_links}): {links[i]}')
        download_link(links[i])


def download_link(link: str, folder='Images'):
    file_name = get_file_name(link)
    page = send_request(link)
    if page is None:
        with open("failed_links.txt", "a") as f:
            f.write(link + '\n')
        return
    if folder != '':
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_name = folder + '/' + file_name
    with open(file_name, 'wb') as f:
        f.write(page.content)


def send_request(link):
    page = None
    for i in range(2):
        try:
            page = requests.get(link)
        except Exception:
            pass
    return page


def get_file_name(link):
    t = link.split('/')
    name = t[-1]
    return name


def get_file_links():
    print('Getting links')
    with open('links.txt') as file:
        links = file.read().splitlines()
    return links


if __name__ == '__main__':
    print('Program started...')
    total_threads_input = int(input('How many threads would you like to have?'))
    beginning_line_input = int(input('Which line do you want to start with? (0 For all lines)'))
    main_threads(total_threads_input, beginning_line_input)
    input('Press Enter to close')
