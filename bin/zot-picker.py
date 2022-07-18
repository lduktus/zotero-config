#!/usr/bin/env python3
# - *-  coding: utf- 8 - *-

# duktus
# 2021

import sys
import argparse
import urllib.request
import urllib.error

NAME = "zot-picker"
BASE_URL = "http://127.0.0.1:23119/better-bibtex/cayw?"
PROBE_URL = "http://127.0.0.1:23119/better-bibtex/cayw?probe=true"
URL_SUFFIX = ""

FORMATS = [
    "asciidoctor-bibtex",
    "biblatex",
    "formatted-citation",
    "formatted-bibliography",
    "json",
    "mmd",
    "pandoc",
    "scannable-cite",
    "translate",
]

DEFAULT_FORMAT = "format=pandoc"

TRANSLATORS = ["biblatex", "csljson"]

def print_error(url):
    print("can't access" + url + "\nis Zotero running and Better BibTex installed?")


def send_request(url):
    try:
        return urllib.request.urlopen(url).read().decode("utf-8")
    except urllib.error.URLError:
        print_error(url)
        sys.exit(1)


def print_formats():
    print(*FORMATS, sep="\n")


# TODO make printformat and format exclusive
# TODO nicer help output, currently it is messy, hence not very helpful
parser = argparse.ArgumentParser(prog=NAME)

parser.add_argument("-f", "--format", choices=FORMATS)
parser.add_argument("-t", "--translator", choices=TRANSLATORS)
parser.add_argument("-c", "--clipboard", action="store_true")
parser.add_argument("-b", "--brackets", action="store_true")
parser.add_argument("-n", "--exportnotes", action="store_true")
parser.add_argument("-p", "--printformats", action="store_true")

args = parser.parse_args()

if args.printformats:
    print_formats()
    sys.exit(0)

# simplify?
if args.format:
    URL_SUFFIX = URL_SUFFIX + "format=" + args.format
else:
    URL_SUFFIX = URL_SUFFIX + DEFAULT_FORMAT

if args.format == "translate":
    if args.translator:
        URL_SUFFIX = URL_SUFFIX + "&" + args.translator
    if args.exportnotes:
        URL_SUFFIX = URL_SUFFIX + "&exportNotes=true"

if args.format == "pandoc" and args.brackets:
    URL_SUFFIX = URL_SUFFIX + "&brackets=true"

if args.clipboard:
    URL_SUFFIX = URL_SUFFIX + "&clipboard=true"

URL = BASE_URL + URL_SUFFIX

if send_request(PROBE_URL) == "ready":
    print(send_request(URL))
else:
    print_error(URL)
