"""
Script to deploy the IDP-Z3 project, to be used whenever there is a new version
ready.

It does the following things:
    * add a tag in git;
    * update version in pyproject.toml;
    * deploy idp-solver module to pypi;
    * deploy IDP-Z3 to GAE;
    * add version in versions.json.

Before actually deploying, it runs the tests to make sure that there are no
errors.

Authors: Pierre Carbonnelle, Simon Vandevelde
"""
from distutils.dir_util import copy_tree
import json
import subprocess
import re


def run(c, **kwargs):
    return subprocess.run(c.split(' '), **kwargs)


def get(c, **kwargs):
    return run(c, capture_output=True, **kwargs).stdout


def require_clean_work_tree(cwd):
    assert 0 == run('git diff-files --quiet --ignore-submodules --', cwd=cwd).returncode, \
        "Cannot deploy: you have unstaged changes."
    assert 0 == run('git diff-index --cached --quiet HEAD --ignore-submodules --', cwd=cwd).returncode, \
        "Cannot deploy: your index contains uncommitted changes."


def query_user(query, default="y", get=False):
    if get is True:
        return input(query)
    if default == "y":
        return input(query) in "Yy"
    else:
        return input(query) in "Nn"


run('python3 test.py generate')

update_statics = query_user("Update the '/IDP-Z3/idp_server/static' folder? (Y/n) ")
if update_statics:
    # Verify we are on master branch.
    branch = get('git rev-parse --abbrev-ref HEAD')
    assert branch == b'master\n', \
        "Cannot deploy: IDP-Z3 not in master branch !"

    # Create new version tag.
    if query_user("Create new tag? (Y/n) "):
        tag_version = query_user("New tag: ", get=True)
        run("git tag {}".format(tag_version))

        # We also need to modify the pyproject.toml.
        with open("./pyproject.toml", "r") as fp:
            pyproject = fp.read()
        pyproject = re.sub(r'version = ".*"',
                           'version = "{}"'.format(tag_version),
                           pyproject)
        with open("./pyproject.toml", "w") as fp:
            fp.write(pyproject)

    if query_user("Deploy idp_server module to Pypi? (Y/n) "):
        run("poetry install")
        run("poetry build")
        run("poetry publish")
        run("rm -rf ./dist")

    # Check if web-IDP-Z3 is on latest version and clean.
    branch = get('git rev-parse --abbrev-ref HEAD', cwd="../web-IDP-Z3")
    assert branch == b'master\n', \
        "Cannot deploy: web-IDP-Z3 not in master branch !"
    require_clean_work_tree("../web-IDP-Z3")

    # Generate static, commit and push it.
    run('npm run -script build', cwd='../web-IDP-Z3', check=True)
    print("Copying to static folder ...")
    copy_tree('../web-IDP-Z3/dist/', './idp_server/static')
    # We don't want to add all files, only the static and the updated tests.
    run("git add ./idp_server/static ./tests")
    run("git commit")
    if query_user("Push to GitLab? (Y/n)"):
        run("git push origin master")

    if query_user("Deploy to Google App Engine? (Y/n) "):

        # if input("Deploy on Heroku ?") in "Yy":
        #     run("git push heroku master")

        # Push to GitLab and GAE.
        run("git push google master")
        if update_statics:
            run("git push google master", cwd='../web-IDP-Z3')
        promote = input("Redirect traffic ? (Y/n) ") in "Yy"
        run(f"gcloud app deploy {'' if promote else '--no-promote'}")

        # update versions.list at https://gist.github.com/IDP-Z3/5d82c61fa39e8aa23da1642a2e2b420a
        versions = get("gcloud app versions list --sort-by=~LAST_DEPLOYED").decode("utf-8")
        id = versions.splitlines()[1].split("  ")[1]
        print("latest version : ", id)
        with open("../5d82c61fa39e8aa23da1642a2e2b420a/versions.json") as json_file:
            data = json.load(json_file)
        data['IDP-Z3 latest'] = f"{id}-dot-interactive-consultant.ew.r.appspot.com"
        with open("../5d82c61fa39e8aa23da1642a2e2b420a/versions.json", "w") as outfile:
            json.dump(data, outfile, indent=4)
        run("git add versions.json" , cwd="../5d82c61fa39e8aa23da1642a2e2b420a")
        run('git commit -m "latest"', cwd="../5d82c61fa39e8aa23da1642a2e2b420a")
        run("git push origin master", cwd="../5d82c61fa39e8aa23da1642a2e2b420a")

        version = '' if promote else f'--version="{id}"'
        run(f"gcloud app browse {version}")
