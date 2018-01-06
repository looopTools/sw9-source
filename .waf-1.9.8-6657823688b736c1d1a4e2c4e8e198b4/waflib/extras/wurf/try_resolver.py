#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
from.error import Error
class TryResolver(object):
	def __init__(self,resolver,ctx,dependency):
		self.resolver=resolver
		self.ctx=ctx
		self.dependency=dependency
	def resolve(self):
		try:
			path=self.resolver.resolve()
		except Error as e:
			self.ctx.logger.debug("Resolve failed in {}:".format(self.resolver),exc_info=True)
			self.ctx.logger.debug(self.dependency)
			error_message=''
			if'current_source'in self.dependency:
				error_message="Current source: {}\n".format(self.dependency.current_source)
			error_message+=e.args[0]
			if not error_message.endswith('\n'):
				error_message+='\n'
			self.dependency.error_messages.append(error_message)
			return None
		except:
			raise
		if path:
			assert os.path.isdir(path)
		else:
			self.ctx.logger.debug("No path returned by {}".format(self.resolver))
		return path
