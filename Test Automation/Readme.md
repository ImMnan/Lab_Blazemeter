Complete automation testing - Shift left

###To start with:

Make sure that you have docker installed, then you can retrieve the docker image by running the following command:
```bash
docker pull digisic/digitalbank
```
Then in order to run the application, use this command:

```bash
docker run -p {host_port}:8080 digisic/digitalbank
```
Making sure to replace with the host port that you'd like to use to access the application. Once the application starts up completely, you can get to the application by directing your browser to http://your_host}:{host_port}/bank/login, so if you're running this locally, you should go to http://localhost: {host_port}/bank/login