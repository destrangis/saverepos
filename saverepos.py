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
import json
import urllib.request


VERSION = "1.1.0"
basedir = "repos"


def get_repos(url, log):
    page = 1
    while 1:
        repos_page = url + "/api/v1/repos/search?page={}".format(page)
        log.debug("Retrieving: {}".format(repos_page))
        rsp = urllib.request.urlopen(repos_page)
        content = json.load(rsp)

        if content["ok"]:
            log.debug("ok - retrieved {} records.".format(len(content["data"])))
        else:
            log.error("NOT OK: {}:".format(repos_page) + json.dumps(content, indent=2))

        if not content["data"]:
            break

        for repo in content["data"]:
            yield repo

        page += 1


def save_repo(repo_obj, basedir, log):
    repo_url = repo_obj["html_url"]
    gitfile = repo_obj["clone_url"]
    owner = repo_obj["owner"]["login"]

    user_backup = os.path.join(basedir, owner)
    if not os.path.isdir(user_backup):
        os.makedirs(user_backup)

    repodir = os.path.basename(repo_url)
    repopath = os.path.join(user_backup, repodir)

    if os.path.isdir(repopath):
        log.info("Updating {}".format(repopath))
        repo_update(repopath, log)
    else:
        log.info("Cloning {}".format(gitfile))
        repo_clone(gitfile, user_backup, log)


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

    for rp in get_repos(opts.url, log):
        save_repo(rp, opts.basedir, log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
