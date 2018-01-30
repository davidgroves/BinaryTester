#!/usr/bin/env python3

import random
from flask import Flask, request
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader(__name__, 'templates'),
    autoescape=select_autoescape(['html', 'xml', 'j2'])
)

app = Flask(__name__)

class Number:
    def __init__(self, value, bits):
        self.value = value
        self.bitcount = bits

    def __add__(self, other):
        return Number(self.value + other.value, self.bitcount)

    def __eq__(self, other):
        if self.value == other.value:
            return True

    def __repr__(self):
        return str(self.value)

    @property
    def binarylist(self):
        binary_string = bin(self.value)[2:].zfill(self.bitcount)
        return list(binary_string)

    @property
    def binarystring(self):
        binary_string = bin(self.value)[2:].zfill(self.bitcount)
        return binary_string

    @classmethod
    def from_bits(cls, bits):
        number = 0
        for i, v in enumerate(reversed(bits)):
            if v == 1:
                number += pow(2,i)

        return Number(number, 8)

################################################################################################

def calc_header(a):
    h = []
    for i in range(8 - 1, -1, -1):
        h.append(pow(2,i))
    return h

@app.route('/add_question.html')
def add_question(bits=8, overflow=False):
    if (overflow == False):
        i = bits - 1
    else:
        i = bits

    a = Number(random.randint(1, pow(2, i) - 1), bits=bits)
    b = Number(random.randint(1, pow(2, i) - 1), bits=bits)
    h = calc_header(a)

    template = env.get_template('base.j2')
    return template.render(header_values=h,
                          a=a,
                          b=b,
                          symbol="+",
                          question = True)

@app.route('/add_answer.html')
def add_answer():
    a = Number(int(request.args['a']), bits=8)
    b = Number(int(request.args['b']), bits=8)
    correct_answer = a + b

    bits = {}
    for i, v in request.args.items():
        if i != 'a' and i != 'b' and i != 'bits':
            bits[int(i)] = int(v)

    print(Number.from_bits(bits=list(bits.values())))
    given_answer = Number.from_bits(bits=list(bits.values()))
    h = calc_header(correct_answer)

    if (correct_answer == given_answer):
        correct = True
    else:
        correct = False

    template = env.get_template('base.j2')
    return template.render(header_values = h,
                           a=a,
                           b=b,
                           correct_answer=correct_answer,
                           given_answer=given_answer,
                           question = False,
                           symbol = "+",
                           correct = correct)

@app.route('/bin2dec_question.html')
def bin2dec_question(bits=8):
    question = Number(random.randint(1, pow(2,bits)), bits)

    template = env.get_template('bin2dec_question.j2')
    return template.render(question=question)

@app.route('/bin2dec_answer.html')
def bin2dec_answer(bits=8):
    question = Number(int(request.args['question']), bits=8)
    answer = Number(int(request.args['answer']), bits=8)

    correct = False
    if question == answer:
        correct = True

    template = env.get_template('bin2dec_answer.j2')
    return template.render(question=question,
                           answer=answer,
                           correct=correct)

@app.route('/dec2bin_question.html')
def dec2bin_question(bits=8):
    question = Number(random.randint(1, pow(2,bits)), bits)

    template = env.get_template('dec2bin_question.j2')
    return template.render(question=question,
                           header_values=calc_header(question))

@app.route('/dec2bin_answer.html')
def dec2bin_answer():
    question = Number(int(request.args['question']), bits=8)

    bits = {}
    for i, v in request.args.items():
        if i != 'question' and i != 'answer' and i != 'bits':
            bits[int(i)] = int(v)

    given_answer = Number.from_bits(bits=list(bits.values()))

    correct = False
    if question == given_answer:
        correct = True

    template = env.get_template('dec2bin_answer.j2')
    return template.render(question=question,
                           answer=given_answer,
                           correct=correct)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host='0.0.0.0')