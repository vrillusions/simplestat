#!/usr/bin/env python

import hmac
from hashlib import sha1
from base64 import b64encode
import json
import sys

dict = {
    'host': 'yuna',
    'uptime': '23325650.14 49101504.30',
    'mem_used': 8000,
    'mem_avail': 245000,
    'disk_used': 29382032,
    'disk_avail': 100000000}

key = 'keep me secret'
msg = json.dumps(dict)
# base64 encode the digest to make it as small as possible
# sha1 is "good enough" because hmac reduces the collision issues
sig = b64encode(hmac.new(key, msg, sha1).digest())

output = "%s // %s" % (msg, sig)
print output

try:
    # split from right in case actual data contains a comment
    input, sig = output.rsplit(' // ', 1)
    decode = json.loads(input)
except ValueError, e:
    # we'll hit this if it can't split it or doesn't like the json data
    print 'Could not parse string, assuming junk'
    # put a debug line here with more info
    sys.exit(1)
print decode
print sig

verifysig = b64encode(hmac.new(key, msg, sha1).digest())

if sig == verifysig:
    print "Signatures match"
else:
    print "Signatures do not match"
    print verifysig.strip()
