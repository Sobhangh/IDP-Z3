from distutils.dir_util import copy_tree
import subprocess

def run(c, **kwargs):
    return subprocess.run(c.split(' '), **kwargs)
def get(c, **kwargs):
    return run(c, capture_output=True, **kwargs).stdout

def require_clean_work_tree(cwd):
    assert 0 == run('git diff-files --quiet --ignore-submodules --', cwd=cwd).returncode, \
        "cannot deploy: you have unstaged changes."
    assert 0 == run('git diff-index --cached --quiet HEAD --ignore-submodules --', cwd=cwd).returncode, \
        "cannot deploy: your index contains uncommitted changes." 

run('python3.8 test.py generate')

branch = get('git rev-parse --abbrev-ref HEAD')
assert branch == b'master\n', "Z3 not in master branch !"


branch = get('git rev-parse --abbrev-ref HEAD', cwd="../autoconfig3")
assert branch == b'master\n', "autoconfig not in master branch !"
require_clean_work_tree("../autoconfig3")

if input("Ready to build and commit ? (Y/n) ") in "Yy":
    run('npm run -script build', cwd='../autoconfig3', check=True)
    print("Copying to static folder ...")
    copy_tree('../autoconfig3/dist/', 'consultant/static')
    run("git add -A")
    run("git commit")

    # if input("Deploy on Heroku ?") in "Yy":
    #     run("git push heroku master")

    if input("Deploy on Google App Engine ? (Y/n)") in "Yy":
        run("git push origin master")
        run("git push google master")
        run("git push google master", cwd='../autoconfig3')
        promote = input("Redirect traffic ? (Y/n)") in "Yy"
        run(f"gcloud app deploy {'' if promote else '--no-promote'}")
        run("gcloud app browse")
