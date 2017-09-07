#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import json
class OnActiveStorePathResolver(object):
	def __init__(self,resolver,dependency,resolve_config_path):
		self.resolver=resolver
		self.dependency=dependency
		self.resolve_config_path=resolve_config_path
	def resolve(self):
		path=self.resolver.resolve()
		self.__write_config(path=path)
		return path
	def __write_config(self,path):
		config_path=os.path.join(self.resolve_config_path,self.dependency.name+'.resolve.json')
		config={'sha1':self.dependency.sha1,'path':path,'is_symlink':self.dependency.is_symlink,'real_path':self.dependency.real_path}
		with open(config_path,'w')as config_file:
			json.dump(config,config_file,indent=4,sort_keys=True)
