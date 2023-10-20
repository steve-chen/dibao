#!/usr/bin/env python3

import sys

class Author(object):
    AUTHOR_KIMBERLEY = 1
    AUTHOR_STEVE = 2
    AUTHOR_HUANG = 3

    def __init__(self, line):
        try:
            author = line.split()[1]
        except IndexError:
            raise KeyError

        if 'Kimberley' in author:
            self.author_id = self.AUTHOR_KIMBERLEY
            self.name = 'Kimberley V'
            self.html = '<div class="chat kimberley">'
        elif 'Yung' in author:
            self.author_id = self.AUTHOR_HUANG
            self.name = '黃永濱Yung Ping Huang'
            self.html = '<div class="chat huang">'
        elif 'Steve' in author:
            self.author_id = self.AUTHOR_STEVE
            self.name = 'Steve Chen'
            self.html = '<div class="chat steve">'
        else:
            raise KeyError

    def is_kimberley(self): return self.author_id is Author.AUTHOR_KIMBERLEY
    def is_huang(self): return self.author_id is Author.AUTHOR_HUANG
    def is_steve(self): return self.author_id is Author.AUTHOR_STEVE

class Line(object):
    def __init__(self, line):
        self.line = line

        try:
            self.decode_author()
            self.decode_timestamp()
            self.decode_message()
        except KeyError:
            self.message = line
            self.author = None
            self.timestamp = None

    def is_new_line(self):
        return self.author is not None

    def decode_timestamp(self):
        self.timestamp = self.line.split()[0]

    def decode_author(self):
        self.author = Author(self.line)

    def decode_message(self):
        if self.author.is_huang():
            self.message = self.line.split(maxsplit=4)[4]
        elif self.author.is_steve() or self.author.is_kimberley():
            self.message = self.line.split(maxsplit=3)[3]
        self.message = self.message[:-1]

    def __str__(self):
        print(self.message)

    def __repr__(self):
        return self.message

    def htmlify(self):
        html = '''
        {}
            <p class="chat-message">
                <span class="timestamp">{} {}</span> {}<br />
            </p>
        </div>'''.format(self.author.html, self.timestamp, self.author.name, self.message)
        return html

lines = []

for each_line in sys.stdin.readlines():
    line = Line(each_line)

    if line.is_new_line() is False:
        lines[-1].message += line.message
    else:
        lines.append(line)

for line in lines:
    print(line.htmlify())
