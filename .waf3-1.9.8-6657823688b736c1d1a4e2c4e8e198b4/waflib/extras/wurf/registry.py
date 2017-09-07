#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import argparse
import os
import json
import hashlib
from collections import OrderedDict
from.git_resolver import GitResolver
from.path_resolver import PathResolver
from.context_msg_resolver import ContextMsgResolver
from.dependency_manager import DependencyManager
from.check_optional_resolver import CheckOptionalResolver
from.on_active_store_path_resolver import OnActiveStorePathResolver
from.on_passive_load_path_resolver import OnPassiveLoadPathResolver
from.try_resolver import TryResolver
from.list_resolver import ListResolver
from.git_checkout_resolver import GitCheckoutResolver
from.git_semver_resolver import GitSemverResolver
from.git_url_parser import GitUrlParser
from.git_url_rewriter import GitUrlRewriter
from.git import Git
from.options import Options
from.mandatory_options import MandatoryOptions
from.mandatory_resolver import MandatoryResolver
from.create_symlink_resolver import CreateSymlinkResolver
from.configuration import Configuration
from.store_lock_path_resolver import StoreLockPathResolver
from.load_lock_path_resolver import LoadLockPathResolver
from.store_lock_version_resolver import StoreLockVersionResolver
from.check_lock_cache_resolver import CheckLockCacheResolver
from.lock_cache import LockCache
from.semver_selector import SemverSelector
from.tag_database import TagDatabase
from.existing_tag_resolver import ExistingTagResolver
from.error import Error
from.error import DependencyError
class RegistryProviderError(Error):
	def __init__(self,name):
		self.name=name
		super(RegistryProviderError,self).__init__("Registry error: {} already added to registry".format(self.name))
class Registry(object):
	class MortalValue:
		def __init__(self,registry,provider_name):
			self.registry=registry
			self.provider_name=provider_name
		def __enter__(self):
			pass
		def __exit__(self,type,value,traceback):
			self.registry.remove(provider_name=self.provider_name)
	providers={}
	cache_providers=set()
	def __init__(self,use_providers=True,use_cache_providers=True):
		self.registry={}
		self.cache={}
		if use_cache_providers:
			for s in Registry.cache_providers:
				self.cache_provider(s)
		if use_providers:
			for k,v in Registry.providers.items():
				self.provide_function(k,v)
	def cache_provider(self,provider_name):
		assert provider_name not in self.cache
		self.cache[provider_name]={}
	def purge_cache(self):
		for provider_name in self.cache:
			self.cache[provider_name]={}
	def provide_function(self,provider_name,provider_function,override=False):
		if not override and provider_name in self.registry:
			raise RegistryProviderError(provider_name)
		def call(**kwargs):
			return provider_function(registry=self,**kwargs)
		self.registry[provider_name]=call
		if provider_name in self.cache:
			self.cache[provider_name]={}
	def provide_value(self,provider_name,value):
		if provider_name in self.registry:
			raise RegistryProviderError(provider_name)
		def call():return value
		self.registry[provider_name]=call
		return Registry.MortalValue(registry=self,provider_name=provider_name)
	def require(self,provider_name,**kwargs):
		if provider_name in self.cache:
			key=frozenset(kwargs.items())
			try:
				return self.cache[provider_name][key]
			except KeyError:
				call=self.registry[provider_name]
				result=call(**kwargs)
				self.cache[provider_name][key]=result
				return result
		else:
			call=self.registry[provider_name]
			result=call(**kwargs)
			return result
	def remove(self,provider_name):
		if provider_name in self.cache:
			del self.cache[provider_name]
		del self.registry[provider_name]
	def __contains__(self,provider_name):
		return provider_name in self.registry
	@staticmethod
	def cache(func):
		Registry.cache_providers.add(func.__name__)
		return func
	@staticmethod
	def provide(func):
		if func.__name__ in Registry.providers:
			raise RegistryProviderError(func.__name__)
		Registry.providers[func.__name__]=func
		return func
@Registry.cache
@Registry.provide
def resolve_path(registry):
	mandatory_options=registry.require('mandatory_options')
	resolve_path=mandatory_options.resolve_path()
	resolve_path=os.path.abspath(os.path.expanduser(resolve_path))
	waf_utils=registry.require('waf_utils')
	waf_utils.check_dir(resolve_path)
	return resolve_path
@Registry.cache
@Registry.provide
def symlinks_path(registry):
	mandatory_options=registry.require('mandatory_options')
	symlinks_path=mandatory_options.symlinks_path()
	symlinks_path=os.path.abspath(os.path.expanduser(symlinks_path))
	waf_utils=registry.require('waf_utils')
	waf_utils.check_dir(symlinks_path)
	return symlinks_path
@Registry.cache
@Registry.provide
def dependency_path(registry,dependency):
	resolve_path=registry.require('resolve_path')
	source=registry.require('source')
	if dependency.resolver=='git':
		git_url_rewriter=registry.require('git_url_rewriter')
		repo_url=git_url_rewriter.rewrite_url(url=source)
		repo_hash=hashlib.sha1(repo_url.encode('utf-8')).hexdigest()[:6]
		name=dependency.name+'-'+repo_hash
	else:
		source_hash=hashlib.sha1(source.encode('utf-8')).hexdigest()[:6]
		name=dependency.name+'-'+source_hash
	dependency_path=os.path.join(resolve_path,name)
	waf_utils=registry.require('waf_utils')
	waf_utils.check_dir(dependency_path)
	return dependency_path
@Registry.cache
@Registry.provide
def git_url_parser(registry):
	return GitUrlParser()
@Registry.cache
@Registry.provide
def git_url_rewriter(registry):
	parser=registry.require('git_url_parser')
	git_protocol=registry.require('git_protocol')
	return GitUrlRewriter(parser=parser,rewrite_protocol=git_protocol)
@Registry.cache
@Registry.provide
def parser(registry):
	return argparse.ArgumentParser(description='Resolve Options',add_help=False)
@Registry.cache
@Registry.provide
def dependency_cache(registry):
	return OrderedDict()
@Registry.cache
@Registry.provide
def lock_cache(registry):
	configuration=registry.require('configuration')
	if configuration.resolver_chain()==Configuration.RESOLVE_AND_LOCK:
		options=registry.require('options')
		return LockCache.create_empty(options=options)
	elif configuration.resolver_chain()==Configuration.RESOLVE_FROM_LOCK:
		project_path=registry.require('project_path')
		lock_path=os.path.join(project_path,Configuration.LOCK_FILE)
		return LockCache.create_from_file(lock_path=lock_path)
	else:
		raise Error("Lock cache not available for {} chain".format(configuration.resolver_chain()))
@Registry.cache
@Registry.provide
def options(registry):
	parser=registry.require('parser')
	args=registry.require('args')
	default_resolve_path=registry.require('default_resolve_path')
	default_symlinks_path=registry.require('default_symlinks_path')
	supported_git_protocols=GitUrlRewriter.git_protocols.keys()
	return Options(args=args,parser=parser,default_resolve_path=default_resolve_path,default_symlinks_path=default_symlinks_path,supported_git_protocols=supported_git_protocols)
@Registry.cache
@Registry.provide
def mandatory_options(registry):
	options=registry.require('options')
	return MandatoryOptions(options=options)
@Registry.cache
@Registry.provide
def semver_selector(registry):
	semver=registry.require('semver')
	return SemverSelector(semver=semver)
@Registry.cache
@Registry.provide
def tag_database(registry):
	ctx=registry.require('ctx')
	return TagDatabase(ctx=ctx)
@Registry.cache
@Registry.provide
def project_git_protocol(registry):
	git=registry.require('git')
	ctx=registry.require('ctx')
	parser=registry.require('git_url_parser')
	try:
		parent_url=git.remote_origin_url(cwd=os.getcwd())
	except Exception as e:
		ctx.to_log('Exception when executing git.remote_origin_url: {}'.format(e))
		return None
	else:
		url=parser.parse(parent_url)
		return url.protocol
@Registry.cache
@Registry.provide
def git(registry):
	git_binary=registry.require('git_binary')
	ctx=registry.require('ctx')
	return Git(git_binary=git_binary,ctx=ctx)
@Registry.cache
@Registry.provide
def git_protocol(registry):
	options=registry.require('options')
	protocol=options.git_protocol()
	if not protocol:
		protocol=registry.require('project_git_protocol')
	if not protocol:
		protocol='https://'
	return protocol
@Registry.provide
def user_path_resolver(registry,dependency):
	mandatory_options=registry.require('mandatory_options')
	path=mandatory_options.path(dependency=dependency)
	ctx=registry.require('ctx')
	dependency.resolver_action='user path'
	resolver=PathResolver(dependency=dependency,path=path)
	return resolver
@Registry.provide
def git_resolver(registry,dependency):
	git=registry.require('git')
	ctx=registry.require('ctx')
	options=registry.require('options')
	dependency_path=registry.require('dependency_path',dependency=dependency)
	git_url_rewriter=registry.require('git_url_rewriter')
	source=registry.require('source')
	return GitResolver(git=git,ctx=ctx,dependency=dependency,source=source,git_url_rewriter=git_url_rewriter,cwd=dependency_path)
@Registry.provide
def resolve_git_checkout(registry,dependency):
	git=registry.require('git')
	ctx=registry.require('ctx')
	dependency_path=registry.require('dependency_path',dependency=dependency)
	if'checkout'in registry:
		checkout=registry.require('checkout')
	else:
		checkout=dependency.checkout
	resolver=registry.require('git_resolver',dependency=dependency)
	resolver=GitCheckoutResolver(git=git,git_resolver=resolver,ctx=ctx,dependency=dependency,checkout=checkout,cwd=dependency_path)
	dependency.resolver_action='git checkout'
	return resolver
@Registry.cache
@Registry.provide
def resolve_git_user_checkout(registry,dependency):
	ctx=registry.require('ctx')
	mandatory_options=registry.require('mandatory_options')
	checkout=mandatory_options.checkout(dependency=dependency)
	with registry.provide_value('checkout',checkout):
		resolver=registry.require('resolve_git_checkout',dependency=dependency)
		resolver=MandatoryResolver(resolver=resolver,msg="User checkout of '{}' failed.".format(checkout),dependency=dependency)
	dependency.resolver_action='git user checkout'
	return resolver
@Registry.provide
def resolve_git_semver(registry,dependency):
	git=registry.require('git')
	ctx=registry.require('ctx')
	semver_selector=registry.require('semver_selector')
	tag_database=registry.require('tag_database')
	source=registry.require('source')
	dependency_path=registry.require('dependency_path',dependency=dependency)
	resolver=registry.require('git_resolver',dependency=dependency)
	resolver=GitSemverResolver(git=git,git_resolver=resolver,ctx=ctx,semver_selector=semver_selector,dependency=dependency,cwd=dependency_path)
	if'steinwurf'in source:
		resolver=ExistingTagResolver(ctx=ctx,dependency=dependency,semver_selector=semver_selector,tag_database=tag_database,resolver=resolver,cwd=dependency_path)
	dependency.resolver_action='git semver'
	return resolver
@Registry.provide
def resolve_git(registry,dependency):
	ctx=registry.require('ctx')
	options=registry.require('options')
	checkout=options.checkout(dependency=dependency)
	if checkout:
		return registry.require('resolve_git_user_checkout',dependency=dependency)
	if'method'in registry:
		method=registry.require('method')
	else:
		method=dependency.method
	method_key="resolve_git_{}".format(method)
	git_resolver=registry.require(method_key,dependency=dependency)
	if options.fast_resolve():
		dependency.resolver_action='fast/'+dependency.resolver_action
		resolve_config_path=registry.require('resolve_config_path')
		fast_resolver=OnPassiveLoadPathResolver(dependency=dependency,resolve_config_path=resolve_config_path)
		fast_resolver=TryResolver(resolver=fast_resolver,ctx=ctx,dependency=dependency)
		return ListResolver(resolvers=[fast_resolver,git_resolver])
	else:
		return git_resolver
@Registry.cache
@Registry.provide
def resolve_from_lock_git(registry,dependency):
	lock_cache=registry.require('lock_cache')
	checkout=lock_cache.checkout(dependency=dependency)
	with registry.provide_value('checkout',checkout),registry.provide_value('method','checkout'):
		resolver=registry.require('resolve_chain',dependency=dependency)
	resolver=CheckLockCacheResolver(resolver=resolver,lock_cache=lock_cache,dependency=dependency)
	return resolver
@Registry.provide
def resolve_from_lock_path(registry,dependency):
	lock_cache=registry.require('lock_cache')
	dependency.rewrite(attribute='resolver',value='lock_path',reason="Using lock file.")
	resolver=registry.require('resolve_chain',dependency=dependency)
	resolver=CheckLockCacheResolver(resolver=resolver,lock_cache=lock_cache,dependency=dependency)
	return resolver
@Registry.provide
def resolve_lock_path(registry,dependency):
	lock_cache=registry.require('lock_cache')
	path=lock_cache.path(dependency=dependency)
	dependency.resolver_action='lock path'
	return PathResolver(dependency=dependency,path=path)
@Registry.provide
def help_chain(registry,dependency):
	ctx=registry.require('ctx')
	resolve_config_path=registry.require('resolve_config_path')
	dependency.resolver_chain='Load'
	dependency.resolver_action='help'
	resolver=OnPassiveLoadPathResolver(dependency=dependency,resolve_config_path=resolve_config_path)
	resolver=TryResolver(resolver=resolver,ctx=ctx,dependency=dependency)
	return resolver
@Registry.provide
def load_chain(registry,dependency):
	ctx=registry.require('ctx')
	resolve_config_path=registry.require('resolve_config_path')
	dependency.resolver_chain='Load'
	resolver=OnPassiveLoadPathResolver(dependency=dependency,resolve_config_path=resolve_config_path)
	resolver=TryResolver(resolver=resolver,ctx=ctx,dependency=dependency)
	resolver=CheckOptionalResolver(resolver=resolver,dependency=dependency)
	return resolver
@Registry.provide
def sources_resolver(registry,dependency):
	ctx=registry.require('ctx')
	resolvers=[]
	for source in dependency.sources:
		with registry.provide_value('source',source):
			resolver_key="resolve_{}".format(dependency.resolver)
			resolver=registry.require(resolver_key,dependency=dependency)
			resolver=TryResolver(resolver=resolver,ctx=ctx,dependency=dependency)
			resolvers.append(resolver)
	resolver=ListResolver(resolvers=resolvers)
	resolver=CheckOptionalResolver(resolver=resolver,dependency=dependency)
	return resolver
@Registry.provide
def resolve_chain(registry,dependency):
	ctx=registry.require('ctx')
	options=registry.require('options')
	resolve_config_path=registry.require('resolve_config_path')
	symlinks_path=registry.require('symlinks_path')
	configuration=registry.require('configuration')
	project_path=registry.require('project_path')
	dependency.resolver_chain='Resolve'
	if options.path(dependency=dependency):
		resolver=registry.require('user_path_resolver',dependency=dependency)
	else:
		resolver=registry.require('sources_resolver',dependency=dependency)
	resolver=CreateSymlinkResolver(resolver=resolver,dependency=dependency,symlinks_path=symlinks_path,ctx=ctx)
	resolver=OnActiveStorePathResolver(resolver=resolver,dependency=dependency,resolve_config_path=resolve_config_path)
	return resolver
@Registry.provide
def resolve_and_lock_chain(registry,dependency):
	resolver=registry.require('resolve_chain',dependency=dependency)
	project_path=registry.require('project_path')
	lock_cache=registry.require('lock_cache')
	lock_type=lock_cache.type()
	if lock_type=='versions':
		return StoreLockVersionResolver(resolver=resolver,lock_cache=lock_cache,dependency=dependency)
	elif lock_type=='paths':
		return StoreLockPathResolver(resolver=resolver,lock_cache=lock_cache,project_path=project_path,dependency=dependency)
	else:
		raise Error("Unknown lock type {}".format(lock_type))
@Registry.provide
def resolve_from_lock_chain(registry,dependency):
	lock_cache=registry.require('lock_cache')
	lock_type=lock_cache.type()
	if lock_type=='versions':
		resolver_key="resolve_from_lock_{}".format(dependency.resolver)
		resolver=registry.require(resolver_key,dependency=dependency)
	elif lock_type=='paths':
		resolver=registry.require('resolve_from_lock_path',dependency=dependency)
	else:
		raise Error("Unknown lock type {}".format(lock_type))
	return resolver
@Registry.provide
def dependency_resolver(registry,dependency):
	ctx=registry.require('ctx')
	configuration=registry.require('configuration')
	resolver_key="{}_chain".format(configuration.resolver_chain())
	resolver=registry.require(resolver_key,dependency=dependency)
	return ContextMsgResolver(resolver=resolver,ctx=ctx,dependency=dependency)
@Registry.provide
def configuration(registry):
	options=registry.require('options')
	args=registry.require('args')
	project_path=registry.require('project_path')
	waf_lock_file=registry.require('waf_lock_file')
	return Configuration(options=options,args=args,project_path=project_path,waf_lock_file=waf_lock_file)
@Registry.provide
def dependency_manager(registry):
	registry.purge_cache()
	ctx=registry.require('ctx')
	dependency_cache=registry.require('dependency_cache')
	options=registry.require('options')
	return DependencyManager(registry=registry,dependency_cache=dependency_cache,ctx=ctx,options=options)
@Registry.provide
def resolve_lock_action(registry):
	lock_cache=registry.require('lock_cache')
	project_path=registry.require('project_path')
	def action():
		lock_path=os.path.join(project_path,Configuration.LOCK_FILE)
		lock_cache.write_to_file(lock_path)
	return action
@Registry.provide
def post_resolver_actions(registry):
	configuration=registry.require('configuration')
	actions=[]
	if configuration.resolver_chain()==Configuration.RESOLVE_AND_LOCK:
		actions.append(registry.require('resolve_lock_action'))
	return actions
def build_registry(ctx,git_binary,default_resolve_path,resolve_config_path,default_symlinks_path,semver,waf_utils,args,project_path,waf_lock_file):
	registry=Registry()
	registry.provide_value('ctx',ctx)
	registry.provide_value('git_binary',git_binary)
	registry.provide_value('default_resolve_path',default_resolve_path)
	registry.provide_value('resolve_config_path',resolve_config_path)
	registry.provide_value('default_symlinks_path',default_symlinks_path)
	registry.provide_value('semver',semver)
	registry.provide_value('waf_utils',waf_utils)
	registry.provide_value('args',args)
	registry.provide_value('project_path',project_path)
	registry.provide_value('waf_lock_file',waf_lock_file)
	return registry
