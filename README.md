# Race Ready application

This application is implemented as a Python3 Flask app, deployed to IBM Cloud with a Cloudant database.

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

Install the dependencies listed in the [requirements.txt](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) file to be able to run the app locally.

Use a [virtual environment](https://packaging.python.org/installing/#creating-and-using-virtual-environments) to avoid having these dependencies clash with those of other Python projects or your operating system and to ensure all following `pip` and `python` commands run with Python3.
```bash
python3 -m venv py3env
source py3env/bin/activate

pip install --upgrade pip # get the latest pip
python -m pip install --user -r requirements.txt
```

## 2.a Testing the app locally
Test cases are written with `pytest` and `tavern` modules and are contained in the `/tests/` directory. The `/pytest.ini` file declares the test cases location to the `pytest` runner.
Run the unit test suite as follows:
```bash
python -m pytest --ignore=tests/fvt  # unit tests only
python apps/app.py & # start app for local tavern tests
python -m pytest --tavern-global-cfg=tests/fvt/config-local.yaml # local tavern tests
```

## 2.b Running the app locally

Run the app.
```bash
python apps/app.py
```

Your app is now running locally and can be viewed at: http://localhost:8000/api/

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

## 5. Database for persistence

The `raceready` application connects to a NoSQL database on IBM Cloud.

* The application's Cloudant service instances and their connected applications are listed under the [`Data & Analytics` section](https://console.bluemix.net/services/cloudantnosqldb/6df81126-94cd-48a7-a94d-dc49621eac7f?paneId=connectedObjects&ace_config=%7B%22region%22%3A%22eu-gb%22%2C%22orgGuid%22%3A%22639a52b7-76ff-42e0-93b8-77353d27bafe%22%2C%22spaceGuid%22%3A%228bb7aeb1-658d-4eb3-9487-faa25d2633fa%22%2C%22redirect%22%3A%22https%3A%2F%2Fconsole.bluemix.net%2Fdashboard%2Fapps%3Fenv_id%3Dibm%253Ayp%253Aeu-gb%22%2C%22bluemixUIVersion%22%3A%22v6%22%2C%22crn%22%3A%22crn%3Av1%3Abluemix%3Apublic%3Acloudantnosqldb%3Aeu-gb%3As%2F8bb7aeb1-658d-4eb3-9487-faa25d2633fa%3A6df81126-94cd-48a7-a94d-dc49621eac7f%3Acf-service-instance%3A%22%2C%22id%22%3A%226df81126-94cd-48a7-a94d-dc49621eac7f%22%7D&env_id=ibm%3Ayp%3Aeu-gb).
* An application instance's connection to a Cloudant service instance is configured in [`Cloud Foundry apps`](https://console.bluemix.net/dashboard/apps?env_id=ibm%3Ayp%3Aeu-gb)/`$app_name`/`Connections`

Environment variables separate deployment settings from source code. For example, instead of hardcoding a database password, this is stored in an environment variable referenced in source code. [Learn more...](/docs/manageapps/depapps.html#app_env)
Database credentials and other connection information is exposed to the application using the `VCAP_SERVICES` environment variable. This environment variable is only available to the application when it is running on IBM Cloud.

## 6. Using the database

Our local application instances can also point to the cloud-hosted database instance(s). A json file stores the credentials for the services the application will use. This file will get used ONLY when the application is running locally. When running in IBM Cloud, the credentials will be read from the VCAP_SERVICES environment variable.

The local-profile file is called `vcap-local.json` in the `apps` directory with the following format:
  ```json
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

The values for `vcap-local.json` come from the IBM Cloud UI, where we select `App -> Connections -> Cloudant -> View Credentials`.
