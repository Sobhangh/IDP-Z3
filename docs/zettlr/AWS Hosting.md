AWS hosting
=
20200401113342

[docs](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)

Benefits:
* auto-scaling
* support for mutiple versions
* time-out control ? yes

Limitations:
* performance ? [CPU power linear](https://docs.aws.amazon.com/lambda/latest/dg/configuration-console.html) with memory configured.  It's for demo anyway
* installation of dReal ? [custom runtimes](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-custom.html)
* 50 MB limit ?

Tools:
* [toolkit for VS Studio](https://aws.amazon.com/fr/visualstudiocode/)
* [flask-lambda](https://github.com/sivel/flask-lambda)

Done:
* create account: pcarbonn-kul
* [create non-root Administrator user](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html) for Account 377556694884
    * will set up AWS Credentials later with aws configure
* [install AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
    * [install Docker](https://docs.docker.com/install/) and [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/): 19.03.8
        * could not give docker access to ec2-user: does not exist
    * install Homebrew 2.2.11
    * install AWS 0.47.0
* give CLI AWS access
    * [install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html) (not SAM CLI !)  
        * [get access keys from IAM console](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) + download accessKeys.csv
        * aws configure with default output: yaml
* install the Amazon toolkit for VSCode, in VSCode
    * did not [set up your AWS credentials](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/setup-credentials.html): already done by aws configure ?
* [create a serverless application](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/create-sam.html):  [hello-world](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)
    * unable to find SAM CLI → restart → ok
    * sam build
    * sam local invoke : ok after a couple of minutes
    * sam deploy –guided
    * deployed [here](https://gb8ubrmp0j.execute-api.us-east-1.amazonaws.com/Prod/hello/) !
* create new version: [here](https://8icksxbl7k.execute-api.eu-west-3.amazonaws.com/Prod/hello/)
    * sam build
    * sam deploy –guided

TODO
* multiple versions ? using [CodeCommit](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html) ?
    * see [versioning an API](https://stackoverflow.com/questions/54208218/versioning-an-api-deployed-with-sam)
* Flask ? see [here](https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80)
    * Use [Beanstalk](https://docs.aws.amazon.com/fr_fr/elasticbeanstalk/latest/dg/Welcome.html) ? [version des applications](https://docs.aws.amazon.com/fr_fr/elasticbeanstalk/latest/dg/applications-versions.html)
* monitoring ?

#hosting