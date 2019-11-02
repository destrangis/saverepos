#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Maintain an updated collection of the GIT repositories in a Gitea server.
"""
import argparse
import os
import os.path
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

VERSION = "1.0.0"
basedir = "repos"

def get_repos(url):
    repos_page = url + "/explore/repos"
    rsp = requests.get(repos_page)
    rsp.raise_for_status()

    soup = BeautifulSoup(rsp.text, "html5lib")
    repo_links = soup.find_all("a", class_="name")
    return [ url + lnk.attrs["href"] for lnk in repo_links ]


def save_repo(repo_url, basedir):
    repodir = os.path.basename(repo_url)
    repopath = os.path.join(basedir, repodir)
    if os.path.isdir(repopath):
        print("Updating {}".format(repo_url))
        repo_update(repopath)
    else:
        print("Cloning {}".format(repo_url))
        gitfile = repo_url + ".git"
        repo_clone(gitfile, basedir)

def repo_clone(repo, basedir):
    savecdir = os.getcwd()
    os.chdir(basedir)

    proc = subprocess.run(["git", "clone", repo])

    os.chdir(savecdir)

def repo_update(repopath):
    savedir = os.getcwd()
    os.chdir(repopath)
    proc = subprocess.run(["git", "pull"])
    os.chdir(savedir)

def cli_options(argv):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--basedir", "-d", metavar="DIR", default=basedir,
                help="Base directory where the repositories will be held.")
    p.add_argument("url", help="URL of the Gitea server.")
    return p.parse_args(argv)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    opts = cli_options(args)

    if not os.path.isdir(opts.basedir):
        os.makedirs(opts.basedir)

    repos = get_repos(opts.url)
    for rp in repos:
        save_repo(rp, basedir)
    return 0

if __name__ == '__main__':
    sys.exit(main())
