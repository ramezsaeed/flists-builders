from js9 import j
import json

j.logger.loggers_level_set(20)
iyo_client = j.clients.itsyouonline.get()
prefab = j.tools.prefab.local
target_path = '/opt/var/build/python3'
install_js9_script = """#!/bin/bash
    set -ex
    export DEBIAN_FRONTEND="noninteractive"
    pushd /opt/code/github/jumpscale
    # installing core and plugins
    for target in core9 lib9 prefab9; do
        pushd ${target}
        %s/bin/pip3 install -e .
        echo "**********"
        echo $target
        echo "**********"
        popd
    done
    popd
    """ % target_path

script = """#!/bin/bash
set -ex
export DEBIAN_FRONTEND="noninteractive"

echo "----------------Python3.6---------------------"
rm -rf /opt/sandbox
mkdir /opt/sandbox
cd /opt/sandbox

wget -O python.tgz https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
tar xzf python.tgz
wget -O zlib.tgz http://www.zlib.net/zlib-1.2.11.tar.gz
tar xzf zlib.tgz
cd zlib-1.2.11
./configure
make
make install


cd /opt/sandbox/Python-3.6.4
./configure --prefix=%s
make
make install

echo "----------------End Python3.6-----------------"


    """ % target_path

def build(prefab):
    """
    Build sandboxed js9
    """
    prefab.core.file_write(content=script, location='/tmp/python_build.sh', mode=0o777)
    prefab.core.run(cmd='bash /tmp/python_build.sh', timeout=7200)
    prefab.core.run(cmd="{}/bin/pip3 install http://home.maxux.net/wheelhouse/g8storclient-1.0-cp36-cp36m-manylinux1_x86_64.whl".format(target_path))
    prefab.core.run(cmd="{}/bin/pip3 install 'git+https://github.com/trezor/python-mnemonic.git'".format(target_path))

    # install IPython
    prefab.core.run(cmd="{}/bin/pip3 install ipython".format(target_path))

    # install js9 on the new python
    prefab.core.run(cmd=install_js9_script, timeout=7200)
    # return

    prefab.core.run("js9 'j.tools.sandboxer.python.do(build=False)'", timeout=1800)


def upload(prefab):
    """
    Uploaded the generated flist, merge it with a base ubuntu image and upload the new full flist
    """
    prefab.core.execute_bash('''curl -b 'caddyoauth=%s' -F file=@/opt/var/build/sandbox/js9_sandbox.tar.gz https://hub.gig.tech/api/flist/me/upload''' % (iyo_client.jwt))
    # zhub_data = {'token_': iyo_client.jwt, 'username': 'abdelrahman_hussein_1','url': 'https://hub.gig.tech/api'}
    # zhub_client = j.clients.zerohub.get(data=zhub_data)
    zhub_client = j.clients.zerohub.get()
    zhub_client.authentificate()
    sources = ['gig-official-apps/ubuntu1604.flist', '{}/js9_sandbox.flist'.format(zhub_client.config.data['username'])]
    target = 'js9_sandbox_full.flist'
    url = '{}/flist/me/merge/{}'.format(zhub_client.api.base_url, target)
    resp = zhub_client.api.post(uri=url, data=json.dumps(sources), headers=None, params=None, content_type='application/json')


def start(prefab):
    build(prefab)
    upload(prefab)

start(prefab)
