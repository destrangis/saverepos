#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Maintain an updated collection of the GIT repositories in a Gitea server.
"""
import argparse
import logging
import os
import os.path
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

VERSION = "1.0.3"
basedir = "repos"


def get_repos(url, log):
    repos_page = url + "/explore/repos"
    log.debug("Retrieving: {}".format(repos_page))
    rsp = requests.get(repos_page)
    rsp.raise_for_status()

    # soup = BeautifulSoup(rsp.text, "html5lib")
    soup = BeautifulSoup(rsp.text, "html.parser")
    repo_links = soup.find_all("a", class_="name")
    return [url + lnk.attrs["href"] for lnk in repo_links]


def save_repo(repo_url, basedir, log):
    repodir = os.path.basename(repo_url)
    repopath = os.path.join(basedir, repodir)
    if os.path.isdir(repopath):
        log.info("Updating {}".format(repopath))
        repo_update(repopath, log)
    else:
        gitfile = repo_url + ".git"
        log.info("Cloning {}".format(gitfile))
        repo_clone(gitfile, basedir, log)


def repo_clone(repo, basedir, log):
    savecdir = os.getcwd()
    os.chdir(basedir)

    proc = subprocess.run(
        ["git", "clone", repo], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    log.debug(proc.stdout)

    os.chdir(savecdir)


def repo_update(repopath, log):
    savedir = os.getcwd()
    os.chdir(repopath)
    proc = subprocess.run(
        ["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    log.debug(proc.stdout)
    os.chdir(savedir)


def cli_options(argv):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--basedir",
        "-d",
        metavar="DIR",
        default=basedir,
        help="Base directory where the repositories will be held.",
    )
    p.add_argument(
        "--loglevel",
        "-l",
        metavar="LEVEL",
        default="ERROR",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    p.add_argument("url", help="URL of the Gitea server.")
    return p.parse_args(argv)


def setup_logging(opts):
    log = logging.getLogger(__name__)
    level = logging.getLevelName(opts.loglevel)
    log.setLevel(level)
    hdl = logging.StreamHandler()
    fmt = logging.Formatter(
        "%(asctime)s:%(name)s:%(levelname)s - %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
    )
    hdl.setFormatter(fmt)
    log.addHandler(hdl)
    return log


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    opts = cli_options(args)
    log = setup_logging(opts)

    if not os.path.isdir(opts.basedir):
        os.makedirs(opts.basedir)

    repos = get_repos(opts.url, log)
    for rp in repos:
        save_repo(rp, opts.basedir, log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
