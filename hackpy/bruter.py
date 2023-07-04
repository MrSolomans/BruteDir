#!/usr/bin/env python3
import sys
import os
import threading
import queue
import requests
import argparse
import textwrap


def get_words(wordlist, words):
    with open(wordlist) as f:
        row_words = f.readlines()
    for word in row_words:
        words.put(word.strip())
    return words

# 爆破类


class Bruter:
    def __init__(self, args, words) -> str:
        self.args = args
        self.words = words

    # 发起请求

    def dir_bruter(self):
        while not self.words.empty():
            url = f'{self.args.url}{self.words.get()}'

            try:
                headers = {
                    'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
                }
                if self.args.proxy:
                    r = requests.get(url, headers=headers,
                                     proxies=self.proxies())
                else:
                    r = requests.get(url, headers=headers)

                if r.status_code == 200:
                    print(f'[*] Seccess {url}: {r.status_code}')
                elif r.status_code == 404 or 403:
                    print(f'[-] Faided {url}: {r.status_code}')
                else:
                    print(f'[+] {url}: {r.status_code}')
            except Exception as e:
                print(f'[!] Error {e}')
                break

    # 请求线程数

    def thread(self):
        for _ in range(self.args.thread):
            t = threading.Thread(target=self.dir_bruter)
            t.start()

    # 使用代理

    def proxies(self):
        try:
            if '@' in self.args.proxy:
                auth, tunnel = self.args.proxy.split('@')
                username, password = auth.split(':')
                proxies_dict = {
                    "http": f"http://{username}:{password}@{tunnel}",
                    "https": f"https://{username}:{password}@{tunnel}"
                }
            else:
                print('[!] ProxyError example: username:password@host:port ')
                sys.exit(0)
        except Exception as e:
            print(f'[!] {e}')
            sys.exit(0)
        return proxies_dict


def main():
    parser = argparse.ArgumentParser(
        description="Arsenal -- Dir Bruter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=textwrap.dedent('''Example:
            bruter.py -u http://baidu.com                                              #使用默认字典爆破域名
            bruter.py -u http://baidu.com -f ./bruterdict.txt                          #配置目录字典
            bruter.py -u http://baidu.com -t 10                                        #配置线程数,默认10线程
            bruter.py -u http://baidu.com -p username:password@host:port               #配置代理
            '''))
    parser.add_argument('-u', '--url', help='要爆破的域名')
    parser.add_argument('-f', '--file', help='配置目录字典')
    parser.add_argument('-t', '--thread', type=int, default=10, help='配置线程数')
    parser.add_argument('-p', '--proxy', help='配置代理')
    args = parser.parse_args()
    words = queue.Queue()
    if args.file:
        bruter = Bruter(args, get_words(args.file, words))
        bruter.thread()
    else:
        wordlist = os.getcwd()+'/php.txt'
        bruter = Bruter(args, get_words(wordlist, words))
        bruter.thread()


if __name__ == '__main__':
    main()
