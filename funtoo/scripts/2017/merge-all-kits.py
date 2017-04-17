#!/usr/bin/python3

import os
from merge_utils import *

fo_path = os.path.realpath(os.path.join(__file__,"../../../.."))

init_kits = [
	{ 'name' : 'core', 'branch' : '1.0-prime', 'source': 'gentoo', 'src_branch' : '355a7986f9f7c86d1617de98d6bf11906729f108', 'date' : '25 Feb 2017' },
	{ 'name' : 'security', 'branch' : '1.0-prime', 'source': 'gentoo', 'src_branch' : '355a7986f9f7c86d1617de98d6bf11906729f108', 'date' : '25 Feb 2017' },
	{ 'name' : 'xorg', 'branch' : '1.17-prime', 'source': 'gentoo', 'src_branch' : 'a56abf6b7026dae27f9ca30ed4c564a16ca82685', 'date' : '18 Nov 2016'  },
	{ 'name' : 'xorg', 'branch' : '1.19-snap', 'source': 'gentoo', 'src_branch' : '355a7986f9f7c86d1617de98d6bf11906729f108', 'date' : '25 Feb 2017' },
	{ 'name' : 'media', 'branch' : '1.0-prime', 'source': 'gentoo', 'src_branch' : '355a7986f9f7c86d1617de98d6bf11906729f108', 'date' : '25 Feb 2017' },
	{ 'name' : 'gnome', 'branch' : '3.20-prime', 'source': 'gentoo', 'src_branch' : '44677858bd088805aa59fd56610ea4fb703a2fcd', 'date' : '08 Sep 2016' },
	{ 'name' : 'perl', 'branch' : '5.24-prime', 'source': 'gentoo', 'src_branch' : 'fc74d3206fa20caa19b7703aa051ff6de95d5588', 'date' : '11 Jan 2017' },
	{ 'name' : 'python', 'branch' : '3.4-prime', 'source': 'gentoo', 'src_branch' : '7fcbdbd8461e5491c89eb18db4ab7a0ec9fa4da6', 'date' : '16 Apr 2017' },
	{ 'name' : 'php', 'branch' : '7.1.3-prime', 'source': 'gentoo', 'src_branch' : '7fcbdbd8461e5491c89eb18db4ab7a0ec9fa4da6', 'date' : '16 Apr 2017' },
	{ 'name' : 'java', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
	{ 'name' : 'dev', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
	{ 'name' : 'kde', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
	{ 'name' : 'desktop', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
	{ 'name' : 'editors', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
	{ 'name' : 'net', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
	{ 'name' : 'text', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
	{ 'name' : 'science', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
	{ 'name' : 'games', 'branch' : 'master', 'source': 'gentoo', 'src_branch' : 'master' },
]

# KIT DESIGN AND DEVELOPER DOCS

# The maintainable model for kits is to have a 'fixups' repository that contains our changes. Then, this file is used to
# automatically generate the kits. Rather than commit directly to the kits, we just maintain fix-ups and this file's meta-
# data.

# We record the source sha1 for creating the fixup from Gentoo. Kit generation should be automated. We simply maintain the
# fix-ups and the source sha1's from gentoo for each branch, and then can have this script regenerate the branches with the
# latest fix-ups. That way, we don't get our changes mixed up with Gentoo's ebuilds.

# A kit is generated from:

# 1. a list of ebuilds, eclasses, licenses to select
# 2. a source repository and SHA1 (we want to map to Gentoo's gentoo-staging repo)
# 3. a collection of fix-ups (from a fix-up repository) that are applied on top (generally, we will replace catpkgs underneath)

# Below, the kits and branches should be defined in a way that includes all this information. It is also possible to
# have a kit that simply is a collection of ebuilds but tracks the latest gentoo-staging. It may or may not have additional
# fix-ups.

# Kits have benefits over shards, in that because they exist on the user's system, they can control which branch they are running
# for each kit. And the goal of the kits is to have a very well-curated selection of relevant packages. At first, we may just
# have a few kits that are carefully selected, and we may have larger collections that we create just to get the curation process
# started. Examples below are text-kit and net-kit, which are very large groups of ebuilds.

# When setting up a kit repository, the 'master' branch is used to store an 'unfrozen' kit that just tracks upstream
# Gentoo. Kits are not required to have a master branch -- we only create one if the kit is designed to offer unfrozen
# ebuilds to Funtoo users.  Examples below are: science-kit, games-kit, text-kit, net-kit.

# If we have a frozen enterprise branch that we are backporting security fixes to only, we want this to be an
# 'x.y-prime' branch. This branch's source sha1 isn't supposed to change and we will just augment it with fix-ups as
# needed.

# As kits are maintained, the following things may change:
#
# 1. The package list may change. This can result in different packages being selected for the kit the next time it
#    is regenerated by this script. We can add mising packages, decide to move packages to other kits, etc. This script
#    takes care of ensuring that all necessary ebuilds and licenses are included when the kit is regenerated.
#
# 2. The fix-ups may change. This allows us to choose to 'fork' various ebuilds that we may need to fix, while keeping
#    our changes separate from the source packages. We can also choose to unfork packages.
#
# 3. Kits can be added or removed.
#
# 4. Kit branches can be created, or alternatively deprecated. We need a system for gracefully deprecating a kit that does
#    not involve deleting the branch. A user may decide to continue using the branch even if it has been deprecated.
#
# 5. Kits can be tagged by Funtoo as being mandatory or optional. Typically, most kits will be mandatory but some effort
#    will be made as we progress to make things like the games-kit or the science-kit optional.
#
# 6. The 'regeneration priority' of kits can be changed. (See below)
#
# 7. The 'catpkg ignore list' of kits can be changed (Not yet implemented.) This would allow python-kit to include all
#    dev-python/* catpkgs except for one or two that should be logically grouped with the gnome-kit, even if python-kit
#    has a 'dev-python/*' selector in its catpkg list.

# 8. A kit git repository may be destroyed and recreated, but keep the same clone URL. This is very likely to happen
#    during the beta period but may also happen in production. Any tool that manages meta-repo submodules should have the
#    ability to detect when a stale repo has been cloned and remove it and replace it with a current clone. I am not sure
#    if git has this functionality built-in, but it could be implemented by our repo management tool by manually recording
#    the SHA1 of the first commit in a branch which can be used to verify whether the repo is in fact current or needs to
#    be re-cloned from the source.

# HOW KITS ARE GENERATED

# Currently, kits are regenerated in a particluar order, such as: "first, core-kit, then security-kit, then perl-kit",
# etc. This script keeps a running list of catpkgs that are inserted into each kit. Once a catpkg is inserted into a
# kit, it is not available to be inserted into successive kits. This design is intended to prevent multiple copies of
# catpkgs existing in multiple kits in parallel. At the end of kit generation, this master list of inserted catpkgs is
# used to prune the 'nokit' repository of catpkgs, so that 'nokit' contains the set of all ebuilds that were not
# inserted into kits.

# THE CODE BELOW CURRENTLY DOESN'T WORK EXACTLY AS DESCRIBED ABOVE! BUT I WANTED TO DOCUMENT THE PLAN FIRST. CODE BELOW NEEDS
# UPDATES TO IMPLEMENT THE DESIGN DEFINED ABOVE.

def auditKit(kit_dict, source_repo, kitted_catpkgs):
	kname = kit_dict['name']
	branch = kit_dict['branch']
	prime = kit_dict['prime'] if 'prime' in kit_dict else False
	if not prime:
		update = True
	else:
		update = kit_dict['update'] if 'update' in kit_dict else True
	kit = GitTree("%s-kit" % kname, branch, "repos@localhost:kits/%s-kit.git" % kname, root="/var/git/dest-trees/%s-kit" % kname, pull=True)

	steps = [
		GitCheckout(branch),
	]

	kit.run(steps)

	actual_catpkgs = set(kit.getAllCatPkgs().keys())
	select_catpkgs = generateAuditSet("%s-kit" % kname, source_repo, pkgdir="/root/funtoo-overlay/funtoo/scripts", branch=branch, catpkg_dict=kitted_catpkgs)

	print("%s : catpkgs selected that are not yet in kit" % kname)
	for catpkg in list(select_catpkgs - actual_catpkgs):
		print(" " + catpkg)
	print()
	print("%s : catpkgs in kit that current do not have a match (possibly because they were pulled in by an earlier kit)" % kname)
	for catpkg in list(actual_catpkgs - select_catpkgs):
		print(" " + catpkg)
	print()


def updateKit(mode, kit_dict, source_repo, kitted_catpkgs):
	kname = kit_dict['name']
	branch = kit_dict['branch']
	prime = kit_dict['prime'] if 'prime' in kit_dict else False
	if 'src_branch' in kit_dict:
		source_repo.run([GitCheckout(kit_dict['src_branch'])])
	if not prime:
		update = True
	else:
		update = kit_dict['update'] if 'update' in kit_dict else True
	kit = GitTree("%s-kit" % kname, branch, "repos@localhost:kits/%s-kit.git" % kname, root="/var/git/dest-trees/%s-kit" % kname, pull=True)

	steps = [
		GitCheckout(branch),
	]

	if update:
		steps += [ CleanTree() ]

	if kname == "core":
		# special extra steps for core-kit:
		steps += [
			GenerateRepoMetadata("core-kit", aliases=["gentoo"], priority=1000),
			SyncDir(source_repo.root, "profiles", exclude=["repo_name"]),
			SyncDir(source_repo.root, "metadata", exclude=["cache","md5-cache","layout.conf"]),
			# grab from the funtoo_overlay that this script is in:
			SyncFiles(fo_path, {
				"COPYRIGHT.txt":"COPYRIGHT.txt",
				"LICENSE.txt":"LICENSE.txt",
			})
		]
	else:
		# non-core repos have slightly different metadata
		steps += GenerateRepoMetadata("%s-kit" % kname, masters=["core-kit"], priority=500),
	
	# from here on in, kit steps should be the same for core-kit and others:

	kit.run(steps)
	if update:
		steps2 = generateShardSteps("%s-kit" % kname, source_repo, kit, clean=False, pkgdir="/root/funtoo-overlay/funtoo/scripts", branch=branch, catpkg_dict=kitted_catpkgs)
		kit.run(steps2)

	a = getAllEclasses(ebuild_repo=kit, super_repo=source_repo)
	l = getAllLicenses(ebuild_repo=kit, super_repo=source_repo)
	# we must ensure all ebuilds are copied ^^^ before we grab all eclasses used:

	steps3 = [
		InsertLicenses(source_repo, select=list(l)),
		InsertEclasses(source_repo, select=list(a)),
		CreateCategories(source_repo),
		GenUseLocalDesc()
	]
		
	if mode == 'prime':
		# only generate metadata cache for prime branches
		steps3 += [ GenCache( cache_dir="/var/cache/git/edb-prime" ) ]

	kit.run(steps3)

	kitted_catpkgs.update(kit.getAllCatPkgs())

	kit.gitCommit(message="updates",branch=branch)

def updateNokitRepo(source_repo):

	# will copy ports-2012 but remove unkitted ebuilds

	nokit = GitTree('nokit', 'master', 'repos@localhost:kits/nokit.git', root="/var/git/dest-trees/nokit", pull=True)

	catpkgs = {} 

	for kit_dict in prime_kits:
		kname = kit_dict['name']
		branch = kit_dict['branch']
		kit = GitTree("%s-kit" % kname, branch, "repos@localhost:kits/%s-kit.git" % kname, root="/var/git/dest-trees/%s-kit" % kname, pull=True)
		catpkgs.update(kit.getAllCatPkgs())
		
	steps = [
		SyncDir(source_repo.root),
		GenerateRepoMetadata("nokit", masters=["core-kit"], priority=-2000),
		RemoveFiles(list(catpkgs.keys())),
		CreateCategories(source_repo),
		GenUseLocalDesc(),
		GenCache( cache_dir="/var/cache/git/edb-prime" )
	]

	nokit.run(steps)
	nokit.gitCommit(message="updates",branch="master")

if __name__ == "__main__":

	import sys

	if len(sys.argv) != 2 or sys.argv[1] not in [ "prime", "update", "audit" ]:
		print("Please specify either 'prime' for funtoo prime kits, or 'update' for updating master branches using gentoo.")
		sys.exit(1)
	elif sys.argv[1] == "prime":
		kits = prime_kits
	elif sys.argv[1] == "update":
		kits = gentoo_kits
	elif sys.argv[1] == "audit":
		kits = prime_kits

	# kitted_catpkgs will store the names of all ebuilds that were moved into kits. We want to remove these from the underlying gentoo repo.
	kitted_catpkgs = {}
	
	for kitdict in kits:
		if not os.path.exists("/var/git/dest-trees/%s-kit" % kitdict['name']):
			print("%s-kit repo not found, skipping..." % kitdict['name'])
			continue
		source_repo = GitTree("ports-2012", "funtoo.org", "repos@localhost:funtoo-overlay.git", reponame="biggy", root="/var/git/dest-trees/ports-2012", pull=True)
		gentoo_staging = GitTree("gentoo-staging", "master", "repos@localhost:ports/gentoo-staging.git", root="/var/git/dest-trees/gentoo-staging", pull=False)

		if kitdict['source'] == 'gentoo':
			src_repo = gentoo_staging
		else:
			src_repo = source_repo
		if sys.argv[1] == "audit":
			auditKit(kitdict, src_repo, kitted_catpkgs)
		else:
			updateKit(sys.argv[1], kitdict, src_repo, kitted_catpkgs)

	if sys.argv[1] == "update":

		updateNokitRepo(source_repo)
		k = sorted(kitted_catpkgs.keys())
		with open("kitted_catpkgs.txt", "w") as a:
			for ki in k:
				a.write(ki+"\n")

# vim: ts=4 sw=4 noet
