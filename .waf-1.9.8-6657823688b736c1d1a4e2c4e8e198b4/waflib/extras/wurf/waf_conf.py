#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

from waflib.Configure import conf
from waflib import Logs
from.import waf_resolve_context
@conf
def dependency_path(ctx,name):
	return waf_resolve_context.dependency_cache[name]['path']
@conf
def is_toplevel(self):
	return self.srcnode==self.path
@conf
def recurse_dependencies(ctx):
	for name,dependency in waf_resolve_context.dependency_cache.items():
		if not dependency['recurse']:
			if Logs.verbose:
				Logs.debug('resolve: Skipped recurse {} cmd={}'.format(name,ctx.cmd))
			continue
		path=dependency['path']
		if Logs.verbose:
			Logs.debug('resolve: recurse {} cmd={}, path={}'.format(name,ctx.cmd,path))
		ctx.recurse([str(path)],once=False,mandatory=False)
