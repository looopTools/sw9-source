#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

from.error import TopLevelError
class MandatoryResolver(object):
	def __init__(self,resolver,msg,dependency):
		self.resolver=resolver
		self.msg=msg
		self.dependency=dependency
	def resolve(self):
		path=self.resolver.resolve()
		if not path:
			raise TopLevelError(msg=self.msg,dependency=self.dependency)
		return path
