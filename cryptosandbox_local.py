from js9 import j 
from time import sleep


def get_prefab_prepared():
    # TODO: for now build on the local machine.
    return j.tools.local.prefab


def do_cryptosandbox_and_push(prefab, flistname="cryptosandbox", bins=None):
    DATA_DIR = '/tmp/cryptosandbox' 
    prefab.blockchain.bitcoin.build()
    prefab.blockchain.bitcoin.install()

    prefab.blockchain.tfchain.build()
    prefab.blockchain.tfchain.install()

    # prefab.blockchain.etherum.build()
    # prefab.blockchain.etherum.install()


    for b in bins:
        j.tools.sandboxer.sandbox_chroot(b, DATA_DIR)

    prefab.core.execute_bash('cd {} && tar -czf /tmp/{}.tar.gz .'.format(DATA_DIR, flistname))
    iyo_client = j.clients.itsyouonline.get()
    prefab.core.execute_bash(
        '''curl -b 'caddyoauth={}' -F file=@/tmp/{}.tar.gz https://hub.gig.tech/api/flist/me/upload'''.format(iyo_client.jwt, flistname)
    )



if __name__ == "__main__":
    prefab = j.tools.prefab.local 
    bins=["/opt/bin/bitcoind", "/opt/bin/bitcoin-cli", "/opt/bin/bitcoin-tx", "/opt/bin/tfchaind", "/opt/bin/tfchainc"]

    do_cryptosandbox_and_push(prefab, flistname="cryptoflist", bins=bins)