#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

class ListResolver(object):
	def __init__(self,resolvers):
		self.resolvers=resolvers
	def resolve(self):
		for resolver in self.resolvers:
			path=resolver.resolve()
			if path:
				return path
		else:
			return None
