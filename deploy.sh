
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  echo 'Not in master branch -> aborting';
  exit 1;
fi

read -p "No pending changes on client and server ? Ready to deploy to CDN ? (Y/n) " -n 1 -r
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
