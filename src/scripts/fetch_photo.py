#!/usr/env python
#coding=utf-8

"""
    Fetch photos from network

    This script is used for fetching photos from xnxyjw.com
"""

import argparse
import logging
import os
import random
import time

from gevent import monkey
monkey.patch_all()
import gevent
import urllib2


photo_location = "http://www.xnxyjw.com/jiaowu/Imgxs/"
photo_extension = "jpg"
out_dir = None
retry_times = 2
out_of_class_range = False
max_fetch_size_per_cls = 60
batch_fetch_size = 20

fetch_grades = ["2010", "2011", "2012"]
major_codes = ["1502", "2351", "2363", "1428", "1432",
               "1429", "1403", "1505", "1410", "1401",
               "1420", "1430", "1421", "1431", "1407",
               "1416", "1435", "1406", "1411", "1424",
               "1412", "1414", "1425", "1437", "1415",
               "1413", "1423", "1433", "1422", "1438",
               "1517", "1436", "1408", "2379", "1518",
               "1426", "1427", "1541", "1419"]


def fetch_photo(stu_id, retried_times=0):
    global out_of_class_range
    if out_of_class_range:
        return
    logging.info("Start to fetching photo of student #%s" % stu_id)
    filename = '%s.%s' % (stu_id, photo_extension)
    photo_url = '%s/%s' % (photo_location, filename)
    try:
        response = urllib2.urlopen(photo_url)
    except urllib2.HTTPError as ex:
        if ex.code == 404:
            logging.info('fetch failed, maybe student id #%s is out of range.' % stu_id)
        elif retried_times < retry_times:
            logging.warning('fetch #%s failed, http code is %s. retry now...' % (stu_id, ex.code))
            fetch_photo(stu_id, retried_times + 1)
        else:
            logging.error('fetch #%s still failed after retry, http code is %s.' % (stu_id, ex.code))
        return

    response_code = response.getcode()
    if response_code == 200:
        file_path = os.path.join(out_dir, filename)
        with open(file_path, 'wb') as out_file:
            out_file.write(response.read())
        logging.info("Finish fetching photo of student #%s" % stu_id)


def fetch_by_cls(grade, major_code, cls):
    global out_of_class_range
    out_of_class_range = False
    logging.info("start to fetch photos of %s%s%s**" % (grade, major_code, cls))
    start = time.time()
    for i in range(0, max_fetch_size_per_cls, batch_fetch_size):
        jobs = [gevent.spawn(fetch_photo, "%s%s%02s%02d" % (grade, major_code, cls, j)) for j in range(i + 1, i + batch_fetch_size + 1)]
        gevent.joinall(jobs, timeout=120)
    end = time.time()
    logging.info("finish fetch photos of %s%s%s**. time used: %s" % (grade, major_code, cls, end - start))


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

    fetch_by_cls(random.choice(fetch_grades),
                 random.choice(major_codes),
                 "01")


if __name__ == '__main__':
    main()
