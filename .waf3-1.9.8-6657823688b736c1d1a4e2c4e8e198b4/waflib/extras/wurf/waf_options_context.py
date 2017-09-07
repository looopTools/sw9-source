#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import sys
import copy
from waflib import Context
from waflib import Options
from.import waf_conf
class WafOptionsContext(Options.OptionsContext):
	def __init__(self,**kw):
		super(WafOptionsContext,self).__init__(**kw)
		self.waf_options=None
		self.wurf_options=None
	def execute(self):
		self.srcnode=self.path
		ctx=Context.create_context('resolve')
		try:
			ctx.execute()
		finally:
			ctx.finalize()
		self.wurf_options=ctx.registry.require('options')
		self.waf_options=self.wurf_options.unknown_args
		self.load('wurf.waf_standalone_context')
		waf_conf.recurse_dependencies(self)
		super(WafOptionsContext,self).execute()
	def is_toplevel(self):
		return self.srcnode==self.path
	def parse_args(self,_args=None):
		assert(_args is None)
		try:
			if self.wurf_options:
				waf_parser=self.parser
				target_group=waf_parser.add_option_group('Resolve options')
				source_group=self.wurf_options.parser._optionals
				for action in source_group._group_actions:
					target_group.add_option(action.option_strings[0],action='store_true'if action.nargs==0 else'store',help=action.help)
		finally:
			super(WafOptionsContext,self).parse_args(_args=self.waf_options)
