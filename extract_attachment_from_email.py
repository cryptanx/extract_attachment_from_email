# -*- coding: utf-8 -*-

import csv
import os
from email.parser import Parser
import hashlib
import email.mime.text
import email.header

DIRECTORY = 'msg'
ATTACHMENT_DIR= 'attach'
OUTPUT_FILE = 'test_result.csv'
ERROR_LOG = 'error_log.csv'

def get_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


def export_to_csv(result, output_file):
    with open(output_file, 'a') as f:
        writecsv = csv.writer(f)
        writecsv.writerow(result)


def get_attachment_file(file):
    email_filename_list = []
    filename_list = []
    sha1_list = []
    msg = email.message_from_file(open(file))
    attachments = msg.get_payload()
    if not os.path.exists(ATTACHMENT_DIR):
        os.mkdir(ATTACHMENT_DIR)
    email_filename_list.append(file)
    for attachment in attachments:
        try:
            fnam = attachment.get_filename()
            f = open(ATTACHMENT_DIR + '/' + fnam, 'wb').write(attachment.get_payload(decode=True,))
            filename_list.append(fnam)
            f.close()
        except Exception as detail:
            pass

    return (email_filename_list, filename_list)


if __name__ == '__main__':
    error_list = []
    for file in get_all_files(DIRECTORY):
        with open(file) as fp:
            contents = []
            contents.append(file)
            headers = Parser().parse(fp)
            contents = get_attachment_file(file)
            try:
                export_to_csv(contents, OUTPUT_FILE)
            except:
                error_list.append(file)
                export_to_csv(error_list, ERROR_LOG)
