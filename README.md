# smtpcredtrap
Simple Python tool to listen on SMTP ports and capture authentication attempts

## Installation and Usage

1. Clone this repo
2. `cd smtpcredtrap`
3. The recommended way to install and run the tool is by using a Python virtual environment to avoid any dependency conflicts:
  - install python3-virtualenv or python3-venv using pip or your operating system's package manager
  - create a virtual environment by running `python3 -m virtualenv .`
  - activate the virtual environment by running `source bin/activate`
  - install the dependencies `pip install -r requirements.txt`
  - ensure that no existing SMTP services are running on your host (eg. exim) and stop them if required
  - run the tool (you will need to run as a privileged user to bind to SMTP ports): `python3 main.py`
  - force apps/services to authenticate with any stored SMTP credentials by changing the SMTP server to the IP of your host and wait for incoming authentication attempts
  - plaintext credentials will be dumped to stdout
4. Alternatively, install the dependencies `pip install aiosmtpd` if you don't want to create a virtual environment and run `python3 main.py`
