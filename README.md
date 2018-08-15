# Race Ready application

This application is implemented as a Python Flask app, deployed to IBM Cloud with a Cloudant database.

## Prerequisites

You'll need the following to contribute:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python 3](https://www.python.org/downloads/)

## 1. Clone the app

Now you're ready to start working with the app. Clone the repo and change to the directory where the sample app is located.
```bash
git clone https://github.com/rosscado/raceready
cd raceready
```

## 2. Run the app locally

Install the dependencies listed in the [requirements.txt](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) file to be able to run the app locally.

You can optionally use a [virtual environment](https://packaging.python.org/installing/#creating-and-using-virtual-environments) to avoid having these dependencies clash with those of other Python projects or your operating system.
```bash
[python3.6] pip install --user -r requirements.txt
```

Run the app.
```bash
python3.6 apps/app.py
```

Your app is now running locally and can be viewed at: http://localhost:8000

## 3. Preparing the app for cloud deployment

The app contains a `manifest.yml` file containing directives for its deployment to IBM Cloud as a CloudFoundry app.

The manifest.yml includes basic information about the app, such as the name, how much memory to allocate for each instance and the route. [Learn more...](https://console.bluemix.net/docs/manageapps/depapps.html#appmanifest)
 ```yaml
 applications:
 - name: raceready
   host: raceready
   memory: 128M
 ```
 The app contains a [`runtime.txt`](https://docs.cloudfoundry.org/buildpacks/python/index.html) file directing CloudFoundry to use a particular version of Python when running the application.

 The app contains a [`requirements.txt`](https://pip.readthedocs.io/en/stable/user_guide/#id1) file listing all the 3rd party Python modules required by the application. These are installed directly with the statement `pip install -r requirements.txt` or automatically by CloudFoundry's Python buildpack.

 The app contains a `Procfile` instructing CloudFoundry's Python buildpack to run a particular [start command](https://docs.cloudfoundry.org/buildpacks/python/index.html) for the webapp. This could alternatively be specified on deploy with `cf push -c $custom_command`.

## 4a. Deploy the app on cloud (automatic)
The application's lifecycle is managed by a [toolchain](https://console.bluemix.net/devops/toolchains/0fc11092-0119-4ab8-a5f0-6cbf19d20e03?env_id=ibm:yp:eu-gb). The tool chain assembles all the project's development tools (git repos, issue tracking, online editors, delivery pipelines, etc.) in one place.

### Delivery Pipeline
The toolchain includes a [Delivery Pipeline](https://console.bluemix.net/devops/pipelines/8de9b026-388d-4ebc-984e-5928d63a1d84?env_id=ibm:yp:eu-gb) that automatically builds, tests, and deploys the application on any commit to the `master` branch.


## 4b. Deploy the app on cloud (manual)

Using the toolchain is recommended, but alternatively you can also use the Cloud Foundry CLI to deploy the app manually.

Choose your API endpoint. Our app is deployed to the UK-South (`eu-gb`) endpoint.
```
cf api https://api.eu-gb.bluemix.net
```
Login to your IBM Cloud account

```
cf login [--sso]
```

From within the *raceready* directory push your app to IBM Cloud
```
cf push
```

This can take a minute. If there is an error in the deployment process you can use the command `cf logs raceready --recent` to troubleshoot.

When deployment completes you should see a message indicating that the app is running.  View your app at the URL listed in the output of the push command.  You can also issue the
  ```
cf apps
  ```
  command to view your apps status and see the URL.

## 5. Add a database

Next, we'll add a NoSQL database to this application and set up the application so that it can run locally and on IBM Cloud.

1. Log in to IBM Cloud in your Browser. Browse to the `Dashboard`. Select your application by clicking on its name in the `Name` column.
2. Click on `Connections` then `Connect new`.
2. In the `Data & Analytics` section, select `Cloudant NoSQL DB` and `Create` the service.
3. Select `Restage` when prompted. IBM Cloud will restart your application and provide the database credentials to your application using the `VCAP_SERVICES` environment variable. This environment variable is only available to the application when it is running on IBM Cloud.

Environment variables enable you to separate deployment settings from your source code. For example, instead of hardcoding a database password, you can store this in an environment variable which you reference in your source code. [Learn more...](/docs/manageapps/depapps.html#app_env)

## 6. Use the database

We're now going to update your local code to point to this database. We'll create a json file that will store the credentials for the services the application will use. This file will get used ONLY when the application is running locally. When running in IBM Cloud, the credentials will be read from the VCAP_SERVICES environment variable.

1. Create a file called `vcap-local.json` in the `get-started-python` directory with the following content:
  ```
  {
    "services": {
      "cloudantNoSQLDB": [
        {
          "credentials": {
            "username":"CLOUDANT_DATABASE_USERNAME",
            "password":"CLOUDANT_DATABASE_PASSWORD",
            "host":"CLOUDANT_DATABASE_HOST"
          },
          "label": "cloudantNoSQLDB"
        }
      ]
    }
  }
  ```

2. Back in the IBM Cloud UI, select your App -> Connections -> Cloudant -> View Credentials

3. Copy and paste the `username`, `password`, and `host` from the credentials to the same fields of the `vcap-local.json` file replacing **CLOUDANT_DATABASE_USERNAME**, **CLOUDANT_DATABASE_PASSWORD**, and **CLOUDANT_DATABASE_URL**.

4. Run your application locally.
  ```
python hello.py
  ```

  View your app at: http://localhost:8000. Any names you enter into the app will now get added to the database.

5. Make any changes you want and re-deploy to IBM Cloud!
  ```
cf push
  ```

  View your app at the URL listed in the output of the push command, for example, *raceready.mybluemix.net*.
