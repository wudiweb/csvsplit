#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
split a big csv file to many small files
you can find the small files in csvsplit directory of the big csv file

this function is just for google import contacts
the default csv header should be: First Name    Last Name   Email Address

@author phychion <http://www.wudiweb.com/>
"""

import os,csv

def calculate_size(file_size,decimal_points=2):
    file_size = int(file_size)
    if file_size > 1024 * 1024 * 1024:
        return u'%s GB' % round(float(file_size) / (1024 * 1024 * 1024),decimal_points)
    elif file_size > 1024 * 1024:
        return u'%s MB' % round(float(file_size) / (1024 * 1024),decimal_points)
    elif file_size > 1024:
        return u'%s KB' % round(float(file_size) / 1024,decimal_points)
    else:
        return '%s Bytes' % round(float(file_size),decimal_points)

def csv_file_split(csv_file,csv_header,split_size=100):
    if not os.path.exists(csv_file):
        print u'Sorry, cannot find this csv file.'

    if csv_header is None or csv_header == '':
        csv_header = u'First Name,Last Name,Email Address'
    else:
        csv_header = csv_header.decode('utf-8')

    print u'Csv file: %s' % csv_file

    csv_file_size = os.path.getsize(csv_file)
    print u"Size: %s\n" % calculate_size(csv_file_size)

    print u'Start to split csv file: '

    csv_save_path = os.path.join(os.path.dirname(csv_file),'csvsplit')
    if not os.path.exists(csv_save_path):
        os.mkdir(csv_save_path)
    print csv_save_path

    csv_file_name = os.path.basename(csv_file)
    csv_new_name = str(csv_file_name).replace(".csv","")

    csv_cnt = 1
    csv_line = 0
    try:
        csv_reader = csv.reader(open(csv_file,"r"))
        for row in csv_reader :
            csv_line += 1
            csv_file_new = os.path.join(csv_save_path,csv_new_name+u'.'+str(csv_cnt)+u'.csv')
            csv_writer = csv.writer(open(csv_file_new,"a+"))
            if csv_line == 1 and csv_header is not None:
                csv_writer.writerows([csv_header.split(','),row])
            else:
                csv_writer.writerow(row)
            if os.path.getsize(csv_file_new) > (int(split_size) * 1000):
                print u'Create csv file: %s, line: %s ' % (os.path.basename(csv_file_new), csv_line)
                csv_cnt += 1
                csv_line = 0
    except Exception: pass

if __name__ == '__main__':
    csv_file = raw_input(u'Please specify the csv file to be split: ')
    split_size = raw_input(u'File Size (KB, default 100KB): ')
    csv_header = raw_input(u'Please type header for csv file (first line, comma separator): ')
    csv_file_split(csv_file.decode('utf-8'),csv_header,split_size)
