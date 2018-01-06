#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import json
import shutil
from.error import Error
class StoreLockVersionResolver(object):
	def __init__(self,resolver,lock_cache,dependency):
		self.resolver=resolver
		self.lock_cache=lock_cache
		self.dependency=dependency
	def resolve(self):
		path=self.resolver.resolve()
		checkout=None
		if self.dependency.git_tag:
			checkout=self.dependency.git_tag
		elif self.dependency.git_commit:
			checkout=self.dependency.git_commit
		else:
			raise Error('Not stable checkout information found.')
		self.lock_cache.add_checkout(dependency=self.dependency,checkout=checkout)
		return path
