# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import gzip
import rarfile
import os

class GUnzipPipeline(object):
    def process_item(self, item, spider):
        if 'files' in item:
            for f in item['files']:
                filename = "{}.xml".format(os.path.splitext(item['name'])[0])
                output_dir = os.path.join(spider.settings['FILES_STORE'], item['store'])
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)
                from_path = os.path.join(spider.settings['FILES_STORE'], f['path'])
                if rarfile.is_rarfile(from_path):
                    rarfile.RarFile(from_path).extractall(output_dir)
                else:
                    to_path = os.path.join(output_dir, filename)
                    cont = gzip.open(from_path, 'rb').read()
                    open(to_path, "wb").write(cont)
                    os.remove(from_path)
        return item
