#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

from waflib import Context
from waflib import Utils
from waflib.Configure import ConfigurationContext
class WafConfigurationContext(ConfigurationContext):
	def __init__(self,**kw):
		super(WafConfigurationContext,self).__init__(**kw)
	def execute(self):
		if not'configure'in Context.g_module.__dict__:
			Context.g_module.configure=Utils.nada
		super(WafConfigurationContext,self).execute()
	def pre_recurse(self,node):
		super(WafConfigurationContext,self).pre_recurse(node)
		if self.is_toplevel():
			self.recurse_dependencies()
