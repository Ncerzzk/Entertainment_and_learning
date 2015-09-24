#!/usr/bin/env python
# coding=utf-8
class Error(BaseException):
    pass

class NoFoundError(Error):
    def __init__(self,what):
        self.what=what
    def __str__(self):
        return "%s not found." %self.what

class AddError(Error):
    def __init__(self,what):
        self.what=what
    def __str__(self):
        return "fail to add %s" %self.what
