# Original code by Fredrik Lundh
# Source: http://effbot.org/zone/bencode.htm

# Modified to work on py3k by Ki-baek Lee (Saberre)

import re


def tokenize(text, match=re.compile(b"([idel])|(\d+):|(-?\d+)").match):
    i = 0
    while i < len(text):
        m = match(text, i)
        s = m.group(m.lastindex)
        i = m.end()
        if m.lastindex == 2:
            yield "s"
            yield text[i:i+int(s)]
            i += int(s)
        else:
            yield s


def decode_item(next, token):
    if isinstance(token, str):
        token = token.encode('ascii')
    if token == b"i":
        # integer: "i" value "e"
        data = int(next())
        if next() != b"e":
            raise ValueError
    elif token == b"s":
        # string: "s" value (virtual tokens)
        raw = next()
        try:
            data = raw.decode('utf-8')
        except:
            data = raw
    elif token == b"l" or token == b"d":
        # container: "l" (or "d") values "e"
        data = []
        tok = next()
        while tok != b"e":
            data.append(decode_item(next, tok))
            tok = next()
        if token == b"d":
            data = dict(zip(data[0::2], data[1::2]))
    else:
        print(token)
        raise ValueError
    return data


def decode(text):
    try:
        src = tokenize(text)
        data = decode_item(src.__next__, src.__next__())
        for token in src: # look for more tokens
            raise SyntaxError("trailing junk")
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("syntax error")
    return data
