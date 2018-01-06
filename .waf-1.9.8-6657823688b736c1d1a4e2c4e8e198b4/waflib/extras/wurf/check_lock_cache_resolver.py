#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

from.error import DependencyError
class CheckLockCacheResolver(object):
	def __init__(self,resolver,lock_cache,dependency):
		self.resolver=resolver
		self.lock_cache=lock_cache
		self.dependency=dependency
	def resolve(self):
		if self.dependency not in self.lock_cache:
			raise DependencyError(msg="Not found in lock cache: {}".format(self.lock_cache),dependency=self.dependency)
		self.lock_cache.check_sha1(dependency=self.dependency)
		return self.resolver.resolve()
