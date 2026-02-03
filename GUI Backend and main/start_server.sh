#!/bin/bash

export PYTHONPATH=/home/cscdev/prod_test

/usr/local/bin/rpyc_classic.py --host 0.0.0.0 -p 12333
