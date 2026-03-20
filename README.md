# Crowdsec DynDNS IP Whitelister

When I started using Crowdsec, I quickly realized some Alerts for my own public IP-address. So I searched the logs and figured out one applications request were detected as brute force attempts. Fortunately, this was not a security issue and just a false positive. A solution was quickly found, but since I have a dynamic external IP-address, I needed a workaround here.

This Python script allows fetching your external IP-address and updating the whitelist automatically. You just need to schedule a Crontab for this script.

## How does it work

The script checks the fetched public IP-address against the address stored in the file `currentIP` if existing, or otherwise creates the file. In case they differ, the newly fetched IP will be written to the file, the `publicIpWhitelist.yaml` file will be updated and the service will be reloaded/container will be restarted.

## Prerequisites

- Crowdsec up and running
- Root access to your machine
- python3
    - requests
    - subprocess
- Crowdsec whitelist configuration installed
  `cscli parsers install crowdsecurity/whitelists`

## How to

1. Install python3 and requests on your Crowdsec machine.
2. Install crowdsecurity/whitelists. Can be done with `sudo cscli parsers install crowdsecurity/whitelists` (already included in Crowdsec Docker version).
3. Copy the `publicIpWhitelister.py`-script to your machine.
4. Adapt the script to your needs (also see configuration).
5. Set up a crontab to automatically run the script in the background
   `*/5 * * * * python3 /path/to/script/publicIpWhitelister.py`
   _(you may need to run it as root)_.
6. Verify your public IP-address was set successfully to the `publicIpWhitelist.yaml` file.
7. Verify the whitelist is listed in the parsers overview `cscli parsers list`.

## See also

- [Crowdsec whitelist docs](https://docs.crowdsec.net/docs/whitelist/intro)
