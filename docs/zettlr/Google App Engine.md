–-
title: Google App Engine
tags: #hosting
   ID: 20200515182231
–-

[Deploying a Flask App](https://medium.com/@dmahugh_70618/deploying-a-flask-app-to-google-app-engine-faa883b5ffab)
[Host multiple versions of your app](https://rominirani.com/app-engine-dev-tips-6-understand-application-versions-d5b195b3f36c)

Done:
* [Console](https://console.cloud.google.com/?_ga=2.171405280.1706200510.1590413868-1723277893.1589396646&pli=1), activate account
* install google-cloud-sdk
    * [download](https://cloud.google.com/sdk/docs#install_the_latest_cloud_tools_version_cloudsdk_current_version) Linux 64 bits and extract to Document/Applications/google-cloud-sdk
    * add to path:
        * Backing up [/home/pcarbonn/.bashrc] to [/home/pcarbonn/.bashrc.backup].
        * [/home/pcarbonn/.bashrc] has been updated.
    * `gcloud components install app-engine-python`
    * `gcloud components update` to version sdk 293
    * `gcloud components install app-engine-python` again
    * create app.yaml, main.py file for [Python3](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/config-files#updating_appyaml)
    * [create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) in the console: 'interactive-consultant' → [dashboard](https://console.cloud.google.com/home/dashboard?project=interactive-consultant)
        * `sudo snap install google-cloud-sdk –classic` : reinstalls everything ?!
        * `gcloud config set project interactive-consultant`
        * update billing information in console / Billing
        * `gcloud auth login`
        * `gcloud services enable cloudbuild.googleapis.com`
        * `gcloud app create --project=interactive-consultant` for europe-west region
        * `gcloud app deploy`
            * error `textx 2.1.0 has requirement click==7.0, but you have click 7.1.2`
            * → add `click==7.0` in requirements.txt
        * `gcloud app browse` → [it works !](https://interactive-consultant.ew.r.appspot.com/)

[Parameters in app.yaml](https://cloud.google.com/appengine/docs/standard/python3/config/appref#entrypoint) for [free tier](https://cloud.google.com/free/docs/gcp-free-tier?hl=fr):
* instance: visible in console / App Engine / Instances (also type of scaling)
    * F4 = 1GB, 2.4 GHz, automatic scaling
* timeout : [depends on type of scaling](https://cloud.google.com/appengine/docs/standard/python/how-instances-are-managed#timeout) automatic = instance of class F → 10 minutes !
* threadsafe ? set [max_concurrent_request](https://cloud.google.com/appengine/docs/standard/python3/config/appref#max_concurrent_requests) to 1 ?
