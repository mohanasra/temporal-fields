#!/usr/bin/env python
import sys
import pdb
import traceback
#sys.path.insert(0, '..')
sys.path.insert(0, '.')
from main import main
from bdb import BdbQuit
import subprocess
subprocess.Popen('find ./exp/.. -iname "*.pyc" -delete'.split())

args = [
    '--name', __file__.split('/')[-1].split('.')[0],  # name is filename
    '--print-freq', '1',
    '--dataset', 'somethingrgb',
    '--arch', 'resnet152',
    '--lr', '.25e-2',
    '--lr-decay-rate', '6',
    '--epochs', '20',
    '--memory-decay', '1.0',
    '--memory-size', '20',
    '--batch-size', '50',
    '--train-size', '0.2',
    '--temporal-weight', '0.03',
    '--temporalloss-weight', '1.2',
    '--window-smooth', '3',
    '--sigma', '300',
    '--val-size', '0.2',
    '--cache-dir', '/glusterfs/gsigurds/ai2/caches/',
    #'--data', '/glusterfs/gsigurds/Something/',
    '--data', '/scratch/gsigurds/somethingsomething/',
    '--train-file', '/nfs.yoda/gsigurds/somethingsomething/something-something-v2-train.json',
    '--val-file', '/nfs.yoda/gsigurds/somethingsomething/something-something-v2-validation.json',
    '--nclass', '174',
    '--pretrained',
    '--adjustment',
    '--balanceloss',
    '--nhidden', '3',
    #'--evaluate',
]
sys.argv.extend(args)
try:
    main()
except BdbQuit:
    sys.exit(1)
except Exception:
    traceback.print_exc()
    print ''
    pdb.post_mortem()
    sys.exit(1)
