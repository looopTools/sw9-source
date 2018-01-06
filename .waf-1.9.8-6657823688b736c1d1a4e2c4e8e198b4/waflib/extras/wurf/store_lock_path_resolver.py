#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import json
import shutil
from.error import Error
class StoreLockPathResolver(object):
	def __init__(self,resolver,lock_cache,project_path,dependency):
		self.resolver=resolver
		self.lock_cache=lock_cache
		self.project_path=project_path
		self.dependency=dependency
	def resolve(self):
		path=self.resolver.resolve()
		self.__check_path(path=path)
		if self.dependency.is_symlink:
			lock_path=self.dependency.real_path
		else:
			lock_path=path
		lock_path=os.path.relpath(path=lock_path,start=self.project_path)
		self.lock_cache.add_path(dependency=self.dependency,path=lock_path)
		return path
	def __check_path(self,path):
		child=os.path.realpath(path)
		parent=os.path.realpath(self.project_path)
		if not child.startswith(parent):
			raise Error("Locked paths must be a within parent project")
