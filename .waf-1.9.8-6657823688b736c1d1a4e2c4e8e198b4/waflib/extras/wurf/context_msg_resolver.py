#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

class ContextMsgResolver(object):
	def __init__(self,resolver,ctx,dependency):
		self.resolver=resolver
		self.ctx=ctx
		self.dependency=dependency
	def resolve(self):
		start_msg='{} "{}"'.format(self.dependency.resolver_chain,self.dependency.name)
		if self.dependency.resolver_action:
			start_msg+=' ({})'.format(self.dependency.resolver_action)
		self.ctx.start_msg(start_msg)
		path=self.resolver.resolve()
		if not path:
			self.ctx.end_msg('Unavailable',color='RED')
		else:
			if self.dependency.is_symlink:
				symlink_path=path
				symlink_node=self.ctx.root.find_dir(str(path))
				if symlink_node.is_child_of(self.ctx.srcnode):
					symlink_path=symlink_node.path_from(self.ctx.srcnode)
				real_path=self.dependency.real_path
				self.ctx.end_msg("{} => {}".format(symlink_path,real_path))
			else:
				self.ctx.end_msg(path)
		return path
