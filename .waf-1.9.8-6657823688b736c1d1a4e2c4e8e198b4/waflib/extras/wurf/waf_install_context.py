#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

from waflib.Build import InstallContext
class WafInstallContext(InstallContext):
	def pre_recurse(self,node):
		super(WafInstallContext,self).pre_recurse(node)
		if self.is_toplevel():
			self.recurse_dependencies()
