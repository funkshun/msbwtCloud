import pysam
import MUSCython
import MUSCython.MultiStringBWTCython as MultiStringBWT
import glob
import pandas as pd
import numpy as np
import os
import time
import csv
import argparse
import socket
import itertools


def bwtsort(atup, btup):
    aseq = atup[0]
    bseq = btup[0]
    for i in xrange(len(aseq)):
        abase = aseq[-1-i]
        bbase = bseq[-1-i]
        if (abase > bbase):
            return 1
        elif (abase < bbase):
            return -1
    else:
        if (atup[1] > btup[1]):
            return 1
        elif (atup[1] < btup[1]):
            return -1
    return 0

def gatherProbes(pf):
    probes = []
    with open(pf, 'rb') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            probes.append((row[0], row[1], row[2]))
    return probes

def sharedPrefixLength(s1, s2):
    # Find the shared prefix length between s1 and s2
    p = 0
    for i in xrange(min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            p += 1
        else:
            break
    return p

def build_stack(msbwt, stack, indices, shared_next, q):
    stack_end = len(stack[-1])
    if shared_next == stack_end:
        # Don't do anything to stack
        lo,hi = indices[-1]
        c = msbwt.countOccurrencesOfSeq(''.join(s for s in reversed(q[stack_end:])), (lo,hi))
    elif shared_next < stack_end:
        # need to cut stack
        lo,hi = indices[-1]
        if q[stack_end:] == '':
            c = hi-lo
        else:
            c = msbwt.countOccurrencesOfSeq(''.join(s for s in reversed(q[stack_end:])), (lo,hi))
        stack = stack[:-(stack_end-shared_next)]
        indices = indices[:-(stack_end-shared_next)]
    else:
        # need to add to stack
        base = stack[-1]
        for i in range(0,shared_next-stack_end):
            p_lo, p_hi = indices[-1]
            stack.append(base+q[stack_end+i])
            if (p_hi-p_lo) == 0: # early termination case
                lo, hi = p_lo, p_hi
            else:
                lo, hi = msbwt.findIndicesOfStr(q[stack_end+i], (p_lo, p_hi))
            indices.append([lo, hi])
            base += q[stack_end+i]
        lo,hi = indices[-1]
        if q[len(stack[-1]):] == '':
            c = hi-lo
        else:
            c = msbwt.countOccurrencesOfSeq(''.join(s for s in reversed(q[len(stack[-1]):])), (lo,hi))
    return stack, indices, c

def get_shared_prefixes(seqs):
    shared = []
    last = seqs[0]
    for seq in seqs[1:]:
        spl = sharedPrefixLength(seq, last)
        shared.append(spl)
        last = seq
    shared.append(0)
    return shared

def generate_counts(msbwt, queries):
    # Takes a list of queries and returns the corresponding counts
    queries = np.array(queries)
    indicesSorted = sorted(range(len(queries)), key=lambda k: queries[k], cmp=bwtsort)
    queriesSorted = sorted(queries, cmp=bwtsort)
    rev = [''.join([s for s in reversed(q)]) for q in queriesSorted]
    # PREPROCESSING STEP: for each query, get prefix index shared with NEXT query
    shared = get_shared_prefixes(rev)
    stack = []
    stack.append('')
    indices = []
    lo, hi = msbwt.findIndicesOfStr('')
    indices.append([lo, hi])
    counts = np.empty((len(queries)), dtype='int32')
    counter = 0
    for row in queriesSorted:
        q = ''.join([s for s in reversed(row)])
        shared_next = shared[counter]
        stack, indices, count = build_stack(msbwt, stack, indices, shared_next, q)
        counts[counter] = count
        counter += 1
    return [int(counts[i]) for i in indicesSorted]
