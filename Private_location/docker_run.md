## Docker installation of a private location agent -OPL/LG

**This is a simple docker run command**
```bash
docker run -d --env HARBOR_ID=<Harbor ID> --env SHIP_ID=<Ship ID> --env AUTH_TOKEN=<Auth Token> --env AUTO_UPDATE=true --env DISTRIBUTION=stable --name=blazemeter-crane --restart=on-failure -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp --net=host blazemeter/crane python agent/agent.py
```

### Proxy settings

Proxy settings env:
```bash
--env HTTP_PROXY=http://server:port 
--env HTTPS_PROXY=http://server:port (or https://server:port)
--env NO_PROXY=127.0.0.1,localhost,myHostname.com
```

Proxy settings if authentication is required:
```bash
--env HTTP_PROXY=http://username:password@server:port 
--env HTTPS_PROXY=https://username:password@server:port
--env NO_PROXY=127.0.0.1,localhost,myHostname.com
```

**This is a docker command with added proxy configurations**
```bash
docker run -d --env HTTP_PROXY=http://server:port --env HTTPS_PROXY=https://server:port --env NO_PROXY=127.0.0.1,localhost,myHostname.com --env HARBOR_ID=<Harbor ID> --env SHIP_ID=<Ship ID> --env AUTH_TOKEN=<Auth Token> --env AUTO_UPDATE=true --env DISTRIBUTION=stable --name=blazemeter-crane --restart=on-failure -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp --net=host blazemeter/crane python agent/agent.py
```

### Configure a Docker Installation to Use CA Bundle

```bash
-e REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt 
-e AWS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
-v /path/to/custom-ca.crt:/etc/ssl/certs/ca-certificates.crt
```
`/path/to/custom-ca.crt` needs to be updated

**This is a docker command with added CA bundle**
```bash
docker run -d -e REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt -e AWS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt --env HARBOR_ID=<Harbor ID> --env SHIP_ID=<Ship ID> --env AUTH_TOKEN=<Auth Token> --env AUTO_UPDATE=true --env DISTRIBUTION=stable --name=blazemeter-crane --restart=on-failure -v /path/to/custom-ca.crt:/etc/ssl/certs/ca-certificates.crt -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp --net=host blazemeter/crane python agent/agent.py
```