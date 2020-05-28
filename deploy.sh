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


BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  echo 'Not in master branch -> aborting';
  exit 1;
fi
require_clean_work_tree

cd ../autoconfig3
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  echo 'Client not in master branch -> aborting';
  exit 1;
fi
require_clean_work_tree
cd ../autoconfigz3

read -p "Ready to build and deploy to CDN ? (Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Building for deployment..."
    cd ../autoconfig3
    npm run -script deploy
    cd ../autoconfigz3
    
    echo "Copying to local and CDN..."
    cp -R ../autoconfig3/dist/* consultant/static
    gsutil -m rsync -r ./consultant/static gs://interactive-consultant/
fi

read -p "Deploy on Google App Engine ? (Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "deploying..."
    git push google master
    gcloud app deploy
    gcloud app browse
fi
