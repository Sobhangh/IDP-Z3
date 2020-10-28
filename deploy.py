from distutils.dir_util import copy_tree
import json
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
        
        # update versions.list at https://gist.github.com/IDP-Z3/5d82c61fa39e8aa23da1642a2e2b420a
        versions = get("gcloud app versions list --sort-by=~LAST_DEPLOYED").decode("utf-8") 
        id = versions.splitlines()[1].split("  ")[1]
        print("latest version : ", id)
        with open("../5d82c61fa39e8aa23da1642a2e2b420a/versions.json") as json_file:
            data = json.load(json_file)
        data['IDP-Z3 latest'] = f"{id}-dot-interactive-consultant.ew.r.appspot.com/"
        with open("../5d82c61fa39e8aa23da1642a2e2b420a/versions.json", "w") as outfile:
            json.dump(data, outfile, indent=4)
        run("git add versions.json" , cwd="../5d82c61fa39e8aa23da1642a2e2b420a")
        run('git commit -m "latest"', cwd="../5d82c61fa39e8aa23da1642a2e2b420a")
        run("git push origin master", cwd="../5d82c61fa39e8aa23da1642a2e2b420a")

        run("gcloud app browse")
