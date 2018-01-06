#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
from.error import DependencyError
class PathResolver(object):
	def __init__(self,dependency,path):
		self.dependency=dependency
		self.path=path
	def resolve(self):
		self.path=os.path.abspath(os.path.expanduser(self.path))
		if not os.path.isdir(self.path):
			raise DependencyError('Path error: "{}" is not a valid ''directory'.format(self.path),dependency=self.dependency)
		return self.path
