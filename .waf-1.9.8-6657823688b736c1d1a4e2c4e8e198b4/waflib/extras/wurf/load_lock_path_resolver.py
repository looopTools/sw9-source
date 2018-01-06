#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import json
from.error import DependencyError
class LoadLockPathResolver(object):
	def __init__(self,dependency,project_path):
		self.dependency=dependency
		self.project_path=project_path
	def resolve(self):
		config=self.__read_config()
		if self.dependency.sha1!=config['sha1']:
			raise DependencyError('Failed sha1 check',self.dependency)
		path=str(config['path'])
		if not os.path.isdir(path):
			raise DependencyError('Invalid path: "{}"'.format(path),self.dependency)
		return path
	def __read_config(self):
		config_path=os.path.join(self.project_path,'resolve_lock_paths',self.dependency.name+'.lock_path.json')
		if not os.path.isfile(config_path):
			raise DependencyError('No lock_path - re-run configure with --lock_paths',self.dependency)
		with open(config_path,'r')as config_file:
			return json.load(config_file)
