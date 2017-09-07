#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

from.error import TopLevelError
class CheckOptionalResolver(object):
	def __init__(self,resolver,dependency):
		self.resolver=resolver
		self.dependency=dependency
	def resolve(self):
		path=self.resolver.resolve()
		if not path and not self.dependency.optional:
			raise TopLevelError(msg="Non-optional dependency failed.",dependency=self.dependency)
		return path
