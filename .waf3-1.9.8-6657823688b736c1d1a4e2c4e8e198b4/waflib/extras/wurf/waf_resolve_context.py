#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import sys
import argparse
import traceback
from collections import OrderedDict
from waflib import Utils
from waflib import Context
from waflib import Options
from waflib import Logs
from waflib import ConfigSet
from waflib import Node
from waflib.Configure import conf
from waflib.Errors import WafError
from.import registry
from.error import CmdAndLogError
from.error import Error
from waflib.extras import semver
dependency_cache=None
class WafResolveContext(Context.Context):
	'''resolves the dependencies specified in the wscript's resolve function'''
	cmd='resolve'
	fun='resolve'
	def __init__(self,**kw):
		super(WafResolveContext,self).__init__(**kw)
	def execute(self):
		if not'resolve'in Context.g_module.__dict__:
			Context.g_module.resolve=Utils.nada
		self.srcnode=self.path
		self.bldnode=self.path.make_node('build')
		self.bldnode.mkdir()
		default_resolve_path=os.path.join(self.path.abspath(),'resolved_dependencies')
		default_symlinks_path=os.path.join(self.path.abspath(),'resolve_symlinks')
		self.registry=registry.build_registry(ctx=self,git_binary='git',semver=semver,default_resolve_path=default_resolve_path,resolve_config_path=self.resolve_config_path(),default_symlinks_path=default_symlinks_path,waf_utils=Utils,args=sys.argv[1:],project_path=self.path.abspath(),waf_lock_file=Options.lockfile)
		Logs.enable_colors(1)
		configuration=self.registry.require('configuration')
		path=os.path.join(self.bldnode.abspath(),configuration.resolver_chain()+'.resolve.log')
		self.logger=Logs.make_logger(path,'cfg')
		self.logger.debug('wurf: Resolve execute {}'.format(configuration.resolver_chain()))
		self.dependency_manager=self.registry.require('dependency_manager')
		try:
			super(WafResolveContext,self).execute()
		except Error as e:
			self.logger.debug("Error in resolve:\n",exc_info=True)
			self.fatal(str(e))
		except:
			raise
		global dependency_cache
		dependency_cache=self.registry.require('dependency_cache')
		self.logger.debug('wurf: dependency_cache {}'.format(dependency_cache))
		post_resolver_actions=self.registry.require('post_resolver_actions')
		for action in post_resolver_actions:
			action()
	def post_recurse(self,node):
		self.dependency_manager.load_dependencies(self.path.abspath(),mandatory=False)
		super(WafResolveContext,self).post_recurse(node)
	def is_toplevel(self):
		return self.srcnode==self.path
	def resolve_config_path(self):
		return self.bldnode.abspath()
	def add_dependency(self,**kwargs):
		self.dependency_manager.add_dependency(**kwargs)
	def cmd_and_log(self,cmd,**kwargs):
		if'cwd'in kwargs:
			cwd=kwargs['cwd']
			kwargs['cwd']=self.root.find_dir(str(cwd))
			assert kwargs['cwd']
		try:
			return super(WafResolveContext,self).cmd_and_log(cmd=cmd,**kwargs)
		except WafError as e:
			raise CmdAndLogError(error=e)
		except:
			raise
