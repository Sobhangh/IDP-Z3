require_clean_work_tree () {
    # Update the index
    git update-index -q --ignore-submodules --refresh
    err=0

    # Disallow unstaged changes in the working tree
    if ! git diff-files --quiet --ignore-submodules --
    then
        echo >&2 "cannot deploy: you have unstaged changes."
        git diff-files --name-status -r --ignore-submodules -- >&2
        err=1
    fi

    # Disallow uncommitted changes in the index
    if ! git diff-index --cached --quiet HEAD --ignore-submodules --
    then
        echo >&2 "cannot deploy: your index contains uncommitted changes."
        git diff-index --cached --name-status -r --ignore-submodules HEAD -- >&2
        err=1
    fi

    if [ $err = 1 ]
    then
        echo >&2 "Please commit or stash them."
        exit 1
    fi
}
python3.8 test.py generate

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  echo 'Not in master branch -> aborting';
  exit 1;
fi
# here, we could require no unstaged changes instead
# require_clean_work_tree

cd ../autoconfig3
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  echo 'Client not in master branch -> aborting';
  exit 1;
fi
require_clean_work_tree
cd ../autoconfigz3

read -p "Ready to build and commit ? (Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Building ..."
    cd ../autoconfig3
    npm run -script build # replace 'build' by 'deploy' to use CDN
    cd ../autoconfigz3
    
    echo "Copying to static folder ..."
    rm -rf consultant/static/*
    cp -R ../autoconfig3/dist/* consultant/static
    git add -A
    git commit # with latest client
    # next line is for CDN
    # gsutil -m rsync -r ./consultant/static gs://interactive-consultant/
fi

read -p "Deploy on Heroku ? (Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "deploying on Heroku..."
    git push heroku master
fi

read -p "Deploy on Google App Engine ? (Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "deploying on Google App Engine..."
    git push google master

    cd ../autoconfig3
    git push google master
    cd ../autoconfigz3

    gcloud app deploy
    gcloud app browse
fi
