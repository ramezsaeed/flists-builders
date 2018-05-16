from js9 import j 
from time import sleep
from jose.jwt import get_unverified_claims
import json


def get_prefab_prepared():
    # TODO: for now build on the local machine.
    return j.tools.local.prefab


iyo_client = j.clients.itsyouonline.get()


def do_pkgsandbox_and_push(prefabpkg, flistname="cryptosandbox", bins=None):
    prefab = prefabpkg.prefab
    DATA_DIR = '/tmp/pkgsandbox' 
    prefab.core.dir_remove(DATA_DIR)
    prefabpkg.build()
    prefabpkg.install()

    for b in bins:
        j.tools.sandboxer.sandbox_chroot(b, DATA_DIR)

    prefab.core.execute_bash('cd {} && tar -czf /tmp/{}.tar.gz .'.format(DATA_DIR, flistname))
    prefab.core.execute_bash(
        '''curl -b 'caddyoauth={}' -F file=@/tmp/{}.tar.gz https://hub.gig.tech/api/flist/me/upload'''.format(iyo_client.jwt, flistname)
    )
    claims = get_unverified_claims(iyo_client.jwt)
    username = claims.get("username", None)

    return "https://hub.gig.tech/{}/{}.flist".format(username, flistname)

if __name__ == "__main__":
    prefab = j.tools.prefab.local 
    bitcoinbins=["/opt/bin/bitcoind", "/opt/bin/bitcoin-cli", "/opt/bin/bitcoin-tx"]
    tfchainbins = ["/opt/bin/tfchaind", "/opt/bin/tfchainc"]
    ethbins = ["/opt/bin/geth"]


    btcflist = do_pkgsandbox_and_push(prefab.blockchain.bitcoin, flistname="bitcoinflist", bins=bitcoinbins)
    tfchainflist = do_pkgsandbox_and_push(prefab.blockchain.tfchain, flistname="tfchainflist", bins=tfchainbins)
    ethereumflist = do_pkgsandbox_and_push(prefab.blockchain.ethereum, flistname="ethereumflist", bins=tfchainbins)

    cryptosources = [btcflist, tfchainflist, ethereumflist]
    zhub_data = {'token_': iyo_client.jwt, 'username': 'thabet','url': 'https://hub.gig.tech/api'}

    zhub_client = j.clients.zhub.get(instance="main", data=zhub_data)
    zhub_client.authentificate()
    sources = [btcflist, tfchainflist, ethereumflist]
    target = 'cryptosandbox.flist'
    url = '{}/flist/me/merge/{}'.format(zhub_client.api.base_url, target)
    resp = zhub_client.api.post(uri=url, data=json.dumps(sources), headers=None, params=None, content_type='application/json')
    print(resp)
