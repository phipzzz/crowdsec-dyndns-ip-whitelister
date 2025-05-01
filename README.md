# Crowdsec DynDNS IP Whitelister

When I started using Crowdsec, I quickly realized some Alerts for my own public IP-address. So I searched the logs and figured out one applications request were detected as brute force attempts. Fortunately, this was not a security issue and just a false positive. A solution was quickly found, but since I have a dynamic external IP-address, I needed a workaround here.

This Python script allows fetching your external IP-address and updating the whitelist automatically. You just need to schedule a Crontab for this script.

## How does it work

The script checks the fetched public IP-address against the address stored in the file `currentIP` if existing, or otherwise creates the file. In case they differ, the newly fetched IP will be written to the file, the `publicIpWhitelist.yaml` file will be updated and the service will be reloaded/container will be restarted.

## Prerequisites

-   Crowdsec up and running
-   Root access to your machine
-   python3
    -   requests
    -   subprocess (already included in Python3 default library)
-   Crowdsec whitelist configuration installed
    `cscli parsers install crowdsecurity/whitelists`

## How to

1. Install python3 and requests on your Crowdsec machine.
2. Install crowdsecurity/whitelists. Can be done with `sudo cscli parsers install crowdsecurity/whitelists` (already included in Crowdsec Docker version).
3. Copy the `publicIpWhitelister.py`-script to your machine.
4. Set up a crontab to automatically run the script in the background
   `*/5 * * * * /usr/bin/python3 /path/to/script/publicIpWhitelister.py`
   _(you may need to run it as root)_.
5. Verify your public IP-address was set successfully to the `publicIpWhitelist.yaml` file.
6. Verify the whitelist is listed in the parsers overview `cscli parsers list`.

## Docker

In case you're using Crowdsec as Docker container, you will need to bind mount `/your/local/path/crowdsec/:etc/crowdsec`. Additionally, edit the script according to your local setup.

```python
crowdsecContainer = True
crowdsecContainerName = "crowdsec" # the name of your container
whitelistsFilePath = "./crowdsec/parsers/s02-enrich/publicIpWhitelist.yaml" # path to publicIpWhitelist.yaml relative to the path of publicIpWhitelister.py
```

The directory structure should look like this:

```bash
├── crowdsec
│   ├── acquis.d
│   ├── acquis.yaml
│   ├── appsec-configs
│   ├── appsec-rules
│   ├── collections
│   ├── config.yaml
│   ├── console
│   ├── console.yaml
│   ├── contexts
│   ├── dev.yaml
│   ├── hub
│   ├── local_api_credentials.yaml
│   ├── notifications
│   ├── online_api_credentials.yaml
│   ├── parsers
│   ├── patterns
│   ├── postoverflows
│   ├── profiles.yaml
│   ├── scenarios
│   ├── simulation.yaml
│   └── user.yaml
├── currentIP # will be created during the first run
├── data
│   ├── crowdsec.db
│   ├── GeoLite2-ASN.mmdb
│   ├── GeoLite2-City.mmdb
│   └── trace -> /staging/var/lib/crowdsec/data/trace
├── docker-compose.yml
├── log
└── publicIpWhitelister-docker.py
```

## Debugging

Append the output of the script to a logfile by adding a filepath to the crontab entry.
`*/5 * * * * /usr/bin/python3 /path/to/script/publicIpWhitelister.py >> /root/crowdsecWhitelister/script.log`

## See also

-   [Crowdsec whitelist docs](https://docs.crowdsec.net/docs/whitelist/intro)
