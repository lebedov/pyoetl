#!/usr/bin/env python

"""
Python wrapper for OrientDB ETL tool.
"""

# Copyright (c) 2015, Lev Givon
# All rights reserved.
# Distributed under the terms of the BSD license:
# http://www.opensource.org/licenses/bsd-license

import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('args', nargs=1)
sys_args = parser.parse_args()

file_name = os.path.realpath(sys_args.args[0])
if not os.environ.has_key('ORIENTDB_DIR'):
    raise ValueError('ORIENTDB_DIR not defined')
ORIENTDB_HOME = os.environ['ORIENTDB_DIR']

JAVA = os.path.join(os.environ['JAVA_HOME'], 'bin/java')
if not os.path.exists(JAVA):
    JAVA = 'java'
ORIENTDB_SETTINGS = ['-Djava.util.logging.config.file='+os.path.join(ORIENTDB_HOME,
                     'config/orientdb-client-log.properties'),
                     '-Djava.awt.headless=true']
if os.environ.has_key('JAVA_OPTS'):
    JAVA_OPTS = [os.environ['JAVA_OPTS']]
else:
    JAVA_OPTS = []

KEYSTORE = os.path.join(ORIENTDB_HOME, 'config/cert/orientdb-console.ks')
KEYSTORE_PASS = 'password'
TRUSTSTORE = os.path.join(ORIENTDB_HOME, 'config/cert/orientdb-console.ts')
TRUSTSTORE_PASS = 'password'
SSL_OPTS = ['-Xmx512m', '-Dclient.ssl.enabled=false', 
            '-Djavax.net.ssl.keyStore=%s' % KEYSTORE,
            '-Djavax.net.ssl.keyStorePassword=%s' % KEYSTORE_PASS,
            '-Djavax.net.ssl.trustStore=%s' % TRUSTSTORE,
            '-Djavax.net.ssl.trustStorePassword=%s' % TRUSTSTORE_PASS]

java_args = [JAVA, '-server']+JAVA_OPTS+ORIENTDB_SETTINGS+SSL_OPTS+\
       ['-Dfile.encoding=utf-8', '-Dorientdb.build.number="@BUILD@"', 
        '-cp', os.path.join(ORIENTDB_HOME, 'lib/*'),
        'com.orientechnologies.orient.etl.OETLProcessor',
        sys.argv[1]]

try:
    ps = subprocess.Popen(java_args, stdout=subprocess.PIPE)
    while ps.poll() is None:
        l = ps.stdout.readline()
        print l,
    print ps.stdout.read()
except Exception as e:
    pass
