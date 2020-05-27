
read -p "No pending changes on client ? Ready to deploy to CDN ? (Y/n) " -n 1 -r
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

read -p "Deploy on GAE ? (Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # do dangerous stuff
    echo "deploying..."
    git push google master
    gcloud app deploy
fi

python3.8 main.py