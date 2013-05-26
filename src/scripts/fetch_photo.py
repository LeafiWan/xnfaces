#!/usr/env python
#coding=utf-8

"""
    Fetch photos from network
"""

import argparse
import logging
import os
import sys
import time

from gevent import monkey; monkey.patch_all()
import gevent
import urllib


photo_location = "http://www.xnxyjw.com/jiaowu/Imgxs/"
photo_extension = "jpg"
out_dir = None


def fetch_photo(stu_id):
    logging.info("Start to fetching photo of student #%s" % stu_id)
    filename = '%s.%s' % (stu_id, photo_extension)
    urllib.urlretrieve('%s/%s' % (photo_location, filename), os.path.join(out_dir, filename))
    logging.info("Finish fetching photo of student #%s" % stu_id)


def test_fetch():
    logging.info("Start test fetch")
    start = time.time()
    prefix = '2009140701'
    for i in range(1, 11):
        stu_id = "%s%02d" % (prefix, i)
        fetch_photo(stu_id)
    end = time.time()
    logging.info("End test fetch")
    logging.info('time used: %s' % (end - start))


def test_gevent_fetch():
    logging.info("Start test fetch")
    start = time.time()
    prefix = '2009140701'
    jobs = [gevent.spawn(fetch_photo, "%s%02d" % (prefix, i)) for i in range(1, 11)]
    gevent.joinall(jobs, timeout=15)
    end = time.time()
    logging.info("End test fetch")
    logging.info('time used: %s' % (end - start))


def init_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)


def main():
    init_logger()
    global out_dir
    parser = argparse.ArgumentParser()
    parser.add_argument('--out-dir', dest="out_dir", type=str)
    args = parser.parse_args()

    out_dir = os.path.abspath(os.path.expanduser(args.out_dir))
    if not os.path.exists(out_dir):
        logging.error('Output directory is invalid.')
        return

    #test_fetch()
    test_gevent_fetch()


if __name__ == '__main__':
    main()
