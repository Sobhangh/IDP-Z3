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
    # Verify we are on main branch.
    branch = get('git rev-parse --abbrev-ref HEAD')
    assert branch == b'main\n', \
        "Cannot deploy: IDP-Z3 not in main branch !"

    # Check if web-IDP-Z3 is on latest version and clean.
    branch = get('git rev-parse --abbrev-ref HEAD', cwd="../web-IDP-Z3")
    assert branch == b'main\n', \
        "Cannot deploy: web-IDP-Z3 not in main branch !"
    require_clean_work_tree("../web-IDP-Z3")

    # Generate static and commit.
    run('npm run -script build', cwd='../web-IDP-Z3', check=True)
    print("Copying to static folder ...")
    copy_tree('../web-IDP-Z3/dist/', './idp_server/static')

    # Create new version tag.
    new_tag = query_user("Create new tag? (Y/n) ")
    if new_tag:
        tag_version = query_user("New tag: ", get=True)
        run(f"git tag {tag_version}")

        # We also need to modify the pyproject.toml.
        with open("./pyproject.toml", "r") as fp:
            pyproject = fp.read()
        pyproject = re.sub(r'version = ".*"',
                           f'version = "{tag_version}"',
                           pyproject)
        with open("./pyproject.toml", "w") as fp:
            fp.write(pyproject)

    # add and commit
    run("git add -A")
    run("git commit")
    run("git push origin main")

    if new_tag:
        # Publish new version on Pypi.
        run("poetry install")
        run("poetry build")
        run("poetry publish")
        run("rm -rf ./dist")

    # if input("Deploy on Heroku ?") in "Yy":
    #     run("git push heroku main")

    if new_tag or query_user("Deploy to Google App Engine? (Y/n) "):
        print("Deploying to GAE")

        # Push to google repository and deploy on GAE.
        run("git push google main")
        run("git push google main", cwd='../web-IDP-Z3')
        run(f"gcloud app deploy {'' if new_tag else '--no-promote'}")

        # update versions.list at https://gist.github.com/IDP-Z3/5d82c61fa39e8aa23da1642a2e2b420a
        versions = get("gcloud app versions list --sort-by=~LAST_DEPLOYED").decode("utf-8")
        id = versions.splitlines()[1].split("  ")[1]
        print("latest version : ", id)
        with open("../5d82c61fa39e8aa23da1642a2e2b420a/versions.json") as json_file:
            data = json.load(json_file)
        data['IDP-Z3 latest'] = f"{id}-dot-interactive-consultant.ew.r.appspot.com"
        if new_tag:
            data[f'IDP-Z3 {tag_version}'] = data['IDP-Z3 latest']
        with open("../5d82c61fa39e8aa23da1642a2e2b420a/versions.json", "w") as outfile:
            json.dump(data, outfile, indent=4)
        run("git add versions.json" , cwd="../5d82c61fa39e8aa23da1642a2e2b420a")
        run('git commit -m "latest"', cwd="../5d82c61fa39e8aa23da1642a2e2b420a")
        run("git push origin main", cwd="../5d82c61fa39e8aa23da1642a2e2b420a")

        # open browser on GAE
        version = '' if new_tag else f'--version="{id}"'
        run(f"gcloud app browse {version}")
