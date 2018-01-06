#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
from.error import Error
class Configuration(object):
	RESOLVE='resolve'
	LOAD='load'
	HELP='help'
	RESOLVE_AND_LOCK='resolve_and_lock'
	RESOLVE_FROM_LOCK='resolve_from_lock'
	LOCK_FILE='lock_resolve.json'
	def __init__(self,project_path,args,options,waf_lock_file):
		self.project_path=project_path
		self.args=args
		self.options=options
		self.waf_lock_file=waf_lock_file
	def resolver_chain(self):
		if self.choose_help():
			return Configuration.HELP
		elif self.choose_resolve_and_lock():
			return Configuration.RESOLVE_AND_LOCK
		elif self.choose_resolve_from_lock():
			return Configuration.RESOLVE_FROM_LOCK
		elif self.choose_resolve():
			return Configuration.RESOLVE
		else:
			return Configuration.LOAD
	def choose_help(self):
		if'-h'in self.args or'--help'in self.args:
			return True
		if'configure'in self.args:
			return False
		waf_lock_path=os.path.join(self.project_path,self.waf_lock_file)
		if not os.path.isfile(waf_lock_path):
			return True
		return False
	def choose_resolve_from_lock(self):
		if not'configure'in self.args:
			return False
		lock_file=os.path.join(self.project_path,'lock_resolve.json')
		if not os.path.isfile(lock_file):
			return False
		return True
	def choose_resolve_and_lock(self):
		if not'configure'in self.args:
			return False
		if self.options.lock_paths()or self.options.lock_versions():
			return True
		return False
	def choose_resolve(self):
		if'configure'in self.args:
			return True
		return False
