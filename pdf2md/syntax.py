# -*- coding: utf8 -*-

import pdb
import re


class BaseSyntax(object):
    def __init__(self):
        pass


    def pattern(self, text):
        return 'plain-text'


    def newline(self, text):
        return True


    def purify(self, text):
        return text.get_text().strip()


class UrbanSyntax(BaseSyntax):
    def __init__(self):
        pass


    def pattern(self, text):
        content = text.get_text().strip()

        if not content:
            return 'none'

        if content.isdigit(): # page number
            return 'none'
        
        # Remove single lines with only numeric identifiers and no content
        num_lines_pattern = r'^([1-9|0-9]+[、.])*(?![\u4e00-\u9fa5a-zA-Z])$'
        if re.search(num_lines_pattern, content):
            return 'none'
        # '^([一二三四五六七八九1-9]+[、.]){3}(?![一二三四五六七八九1-9]).*([\u4e00-\u9fa5a-zA-Z]+)$'
        h4_pattern = r'^([1-9|0-9]+[、.]){3}(?![1-9|0-9]).*([\u4e00-\u9fa5a-zA-Z]+)$'
        if 24.0 < text.height < 26.0:
            return 'heading-1'

        if 22.0 < text.height < 24.0:
            return 'heading-2'

        if 16.0 < text.height < 18.0:
            return 'heading-3'

        if (14.0 < text.height < 16.0) and (text.x0 < 90.1) and (re.search(h4_pattern, content)):
            return 'heading-4'
        
        ol_pattern = r'^\d+、'
        if re.search(ol_pattern, content):
            return 'ordered-list-item'

        return 'plain-text'


    def newline(self, text):
        if text.x1 > 505.0: # reach the right margin
            return False

        return True


    def purify(self, text):
        content = text.get_text().strip()

        h_pattern = re.search('^(# )(.*)$', content)
        if h_pattern:
            return h_pattern.group(2)
        
        return content

