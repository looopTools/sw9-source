#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import json
from.error import DependencyError
class OnPassiveLoadPathResolver(object):
	def __init__(self,dependency,resolve_config_path):
		self.dependency=dependency
		self.resolve_config_path=resolve_config_path
	def resolve(self):
		config=self.__read_config()
		if self.dependency.sha1!=config['sha1']:
			raise DependencyError('Failed sha1 check',self.dependency)
		if config['is_symlink']:
			self.dependency.is_symlink=config['is_symlink']
			self.dependency.real_path=str(config['real_path'])
		path=str(config['path'])
		if not os.path.isdir(path):
			raise DependencyError('Invalid path: "{}"'.format(path),self.dependency)
		return path
	def __read_config(self):
		config_path=os.path.join(self.resolve_config_path,self.dependency.name+'.resolve.json')
		if not os.path.isfile(config_path):
			raise DependencyError('No config - re-run configure',self.dependency)
		with open(config_path,'r')as config_file:
			return json.load(config_file)
