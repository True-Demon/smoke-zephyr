#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  workshop/argparse_types.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import argparse
import binascii
import logging
import os
import re

from . import is_valid_email_address
from . import parse_timespan

class RegexType(object):
	"""An argparse type representing an arbitrary string which matches the specified regex."""
	def __init__(self, regex, error_message=None):
		self.regex = regex
		self.error_message = (error_message or "{arg} is not valid")

	def __call__(self, arg):
		if hasattr(self.regex, 'match'):
			result = self.regex.match(arg)
		else:
			result = re.match(self.regex, arg)
		if not result:
			raise argparse.ArgumentTypeError(self.error_message.format(arg=repr(arg)))
		return arg

def bin_b64_type(arg):
	"""An argparse type representing binary data encoded in base64."""
	try:
		arg = base64.standard_b64decode(arg)
	except (binascii.Error, TypeError):
		raise argparse.ArgumentTypeError("{0} is not valid base64 data".format(repr(arg)))
	return arg

def bin_hex_type(arg):
	"""An argparse type representing binary data encoded in hex."""
	try:
		arg = binascii.a2b_hex(arg)
	except (binascii.Error, TypeError):
		raise argparse.ArgumentTypeError("{0} is not valid hex data".format(repr(arg)))
	return arg

def dir_type(arg):
	"""An argparse type representing a valid directory."""
	if not os.path.isdir(arg):
		raise argparse.ArgumentTypeError("{0} is not a valid directory".format(repr(arg)))
	return arg

def email_type(arg):
	"""An argparse type representing an email address."""
	if not is_valid_email_address(arg):
		raise argparse.ArgumentTypeError("{0} is not a valid email address".format(repr(arg)))
	return arg

def log_level_type(arg):
	"""An argparse type representing a logging level."""
	if not arg.upper() in ('NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
		raise argparse.ArgumentTypeError("{0} is not a valid log level".format(repr(arg)))
	return getattr(logging, arg.upper())

def port_type(arg):
	"""An argparse type representing a tcp or udp port number."""
	if not arg.isdigit():
		raise argparse.ArgumentTypeError("{0} is not a valid port".format(repr(arg)))
	arg = int(arg)
	if arg < 0 or arg > 65535:
		raise argparse.ArgumentTypeError("{0} is not a valid port".format(repr(arg)))
	return arg

def timespan_type(arg):
	"""An argparse type representing a timespan such as 6h for 6 hours."""
	try:
		arg = parse_timespan(arg)
	except ValueError:
		raise argparse.ArgumentTypeError("{0} is not a valid time span".format(repr(arg)))
	return arg
