# sandbox

## requirements

### openvcloud configuration

make sure your js9_config has been configured

if not do

```bash
js9_config init
```

if you don't know do

```bash
js9_config check
```



it will ask the right questions

## check that openvcloud client works

will check that you have instances configured

```bash
js9_config list -l j.clients.openvcloud -d
```

it will print errors if any issues

## to change configuration info

```bash
js9_config configure -l j.clients.openvcloud -i test
```

- '-i' is the instance

## how to get your jwt token?

```
js9 'print(j.clients.itsyouonline.default.jwt_get())'
```

## to test do

```
js9 'cl=j.clients.openvcloud.get(instance="test");sp=cl.space_get()'
```

this will get your space if you don't see an error it means you have access to this space on openvcloud

fyi:

```yaml
configmanager:

- path: /Users/kristofdespiegeleer/code/docs/despiegk/config_despiegk
- keyname: kds
- is sandbox: False
- sshagent loaded: True
- key in sshagent: True

configuration items for j.clients.openvcloud

 - test
    config:j.clients.openvcloud:test


        account = 'despiegk'

        address = 'be-gen-1.demo.greenitglobe.com'

        jwt_ = '...'

        location = 'be-gen-1'

        port = 443

        space = 'test'

```

## an example script to create a node on OVC

```python
cl=j.clients.openvcloud.get(instance="test")
sp=cl.space_get()

```

copy paste in js9 shell

## An example to run sandboxing on the local machine

First you need to make sure that you have the zero-hub client installed locally
```python
pip install -e 'git+https://github.com/zero-os/0-hub#egg=zerohub&subdirectory=client'
```

Then you need to make sure that the zero-hub client is configured correclty
```python
iyo_client = j.clients.itsyouonline.get('main')
zhub_data = {'token_': iyo_client.jwt, 'username': <iyo_username>,'url': 'https://hub.gig.tech/api'}
zhub_client = j.clients.zerohub.get(data=zhub_data)
zhub_client.config.save()
```

This will run the sandboxing of js9 on the local machine without the need of a remote machine.
To run the script please run the following command after cloning the sandbox repo:
```python
python3 /opt/code/github/jumpscale/sandbox/sandbox_js9_local.py
```

The script will do the following:
- create the js9 sandbox flist and upload it to the current user's (configured via IYO) account at https://hub.gig.tech/
- merge the uploaded flist with a base ubuntu 16.04 flist (gig-official-apps/ubuntu1604-for-js.flist)
- upload the merged flist as <username>/js9_sandbox_full.flist

### Testing the sandbox
To test the uploaded flist you can use the zbundle tool from https://github.com/zero-os/0-bundle 
After creating the sandbox, a flist for js9 will be uploaded to your account on your account at https://hub.gig.tech

#### Installing Zbundle
To install the zbundle tool you need to execute the following steps:
```bash
mkdir -p /opt/bin
wget -O /opt/bin/zbundle https://download.gig.tech/zbundle
cd /opt/bin
chmod +x zbundle
```

#### Testing the sandbox via zbundle
Then you can start your sandbox using the following command
```bash
cd /opt/bin
zbundle -id js9sandbox --entry-point /bin/bash --no-exit https://hub.gig.tech/abdelrahman_hussein_1/js9_sandbox_full.flist
```
You should change abdelrahman_hussein_1 from the above command with your own IYO username.
Once started you can use chroot to use the sandboxed environment
```bash
chroot /tmp/zbundle/js9sandbox
```
Once you are already chrooted, then you can start a js9 shell session using the following command
```bash
source /env.sh; js9
```
You can also run the capacity reporting tool using the following command
```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf; source env.sh ; js9 'print(j.sal.ubuntu.capacity.report())'
```
