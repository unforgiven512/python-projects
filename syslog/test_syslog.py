#!/usr/bin/env python3

import os
import sys
import time
import datetime
import argparse
import logging
import syslog

prg_name = 'python-syslog-test'
ver_major = 0
ver_minor = 1
ver_patch = 0


def main():
    print("===== %s (v%d.%d.%d) =====\n\n" % (prg_name, ver_major, ver_minor, ver_patch))
    syslog.openlog(ident=prg_name, logoption=(syslog.LOG_PID | syslog.LOG_NDELAY | syslog.LOG_CONS), facility=syslog.LOG_USER)
    syslog.syslog("hello world")

if __name__ == "__main__":
    main()
