#!/usr/bin/env python

"""
Python wrapper for OrientDB ETL tool.
"""

# Copyright (c) 2015-2016, Lev Givon
# All rights reserved.
# Distributed under the terms of the BSD license:
# http://www.opensource.org/licenses/bsd-license

import argparse
import glob
import os
import subprocess
import sys

class OETLProcessor(object):
    """
    OrientDB ETL Python wrapper.

    Parameters
    ----------
    ORIENTDB_DIR : str
        Directory of OrientDB installation.
    JAVA : str
        Path to `java` executable.
    JAVA_OPTS : list
        Options to pass to `java`.
    
    Methods
    -------
    process(file_name, out=False)
        Run ETL on specified JSON config file.
    """

    def __init__(self, ORIENTDB_DIR, JAVA='java', JAVA_OPTS=[]):
        # Check if the specified OrientDB home directory actually contains the
        # ETL JAR:
        if not glob.glob(os.path.join(ORIENTDB_DIR, 'lib/orientdb-etl-*.jar')):
            raise ValueError('invalid OrientDB home directory')

        ORIENTDB_SETTINGS = ['-Djava.util.logging.config.file='+os.path.join(ORIENTDB_DIR,
                             'config/orientdb-client-log.properties'),
                             '-Djava.awt.headless=true']

        KEYSTORE = os.path.join(ORIENTDB_DIR, 'config/cert/orientdb-console.ks')
        KEYSTORE_PASS = 'password'
        TRUSTSTORE = os.path.join(ORIENTDB_DIR, 'config/cert/orientdb-console.ts')
        TRUSTSTORE_PASS = 'password'
        SSL_OPTS = ['-Xmx512m', '-Dclient.ssl.enabled=false', 
                    '-Djavax.net.ssl.keyStore=%s' % KEYSTORE,
                    '-Djavax.net.ssl.keyStorePassword=%s' % KEYSTORE_PASS,
                    '-Djavax.net.ssl.trustStore=%s' % TRUSTSTORE,
                    '-Djavax.net.ssl.trustStorePassword=%s' % TRUSTSTORE_PASS]
        self._java_args = [JAVA, '-server']+JAVA_OPTS+ORIENTDB_SETTINGS+SSL_OPTS+\
                          ['-Dfile.encoding=utf-8', '-Dorientdb.build.number="@BUILD@"', 
                           '-cp', os.path.join(ORIENTDB_DIR, 'lib/*'),
                           'com.orientechnologies.orient.etl.OETLProcessor']

    def process(self, file_name, out=False):
        """
        Process a file with OrientDB ETL. 

        Parameters
        ----------
        file_name : str
            Path to OrientDB JSON config file.
        out : bool
            Display output if `out` is True.

        Returns
        -------
        r : int
            Execution return code.
        """
        
        args = self._java_args+[file_name]
        if out:
            ps = subprocess.Popen(args, stdout=subprocess.PIPE)
            while ps.poll() is None:
                l = ps.stdout.readline()
                print l,
            print ps.stdout.read()
            return ps.returncode
        else:
            with open(os.devnull, 'w') as fp:
                return subprocess.Popen(args, stdout=fp).wait()

def main():
    description = "OrientDB ETL tool (Python version)."
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument('-d', help="Display command output.", action='store_true')
    parser.add_argument('args', nargs='+', help="OrientDB JSON config files")
    args = parser.parse_args()

    if not os.environ.has_key('ORIENTDB_DIR'):
        raise ValueError('ORIENTDB_DIR not defined')
    ORIENTDB_DIR = os.environ['ORIENTDB_DIR']

    JAVA = os.path.join(os.environ['JAVA_HOME'], 'bin/java')
    if not os.path.exists(JAVA):
        JAVA = 'java'
    if os.environ.has_key('JAVA_OPTS'):
        JAVA_OPTS = [os.environ['JAVA_OPTS']]
    else:
        JAVA_OPTS = []

    p = OETLProcessor(ORIENTDB_DIR, JAVA, JAVA_OPTS)
    if args.d:
        out = True
    else:
        out = False
    for file_name in args.args:
        p.process(os.path.realpath(file_name), out)

