from urllib.parse import urljoin
import urllib3
import json

import pyradapi.schema as sc

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# standard posting payload
def post_payload(url: str, payload: dict = dict()):
    http = urllib3.PoolManager()
    resp = http.request(
        method="POST",
        url=url,
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload),
    )
    return json.loads(resp.data.decode("utf-8"))


class Payload:
    def __init__(self, url: str, payload: str) -> None:
        self.payload = payload
        self.url = url

    def __repr__(self) -> str:
        return f"url:\t\t{self.url} \npayload:\t{json.dumps(self.payload)}"


class GatewayTokenPayloads:
    def __init__(self, network: str, url: str):
        self.network = network
        self.url = urljoin(url, "token/")
        assert self.url[-1] == "/"

    def native(self, **at_state_identifier):
        return Payload(
            urljoin(self.url, "native"),
            {
                **sc.network_identifier(self.network),
                **sc.at_state_identifier(**at_state_identifier),
            },
        )

    def derive(self, hex: str, symbol: str):
        return Payload(
            urljoin(self.url, "derive"),
            {
                **sc.network_identifier(self.network),
                **sc.public_key(hex),
                "symbol": symbol,
            },
        )

    def __call__(self, rri: str, **at_state_identifier):
        return Payload(
            self.url,
            {
                **sc.network_identifier(self.network),
                **sc.token_identifier(rri),
                **sc.at_state_identifier(**at_state_identifier),
            },
        )


class GatewayAccountPayloads:
    def __init__(self, network: str, url: str):
        self.network = network
        self.url = urljoin(url, "account/")
        assert self.url[-1] == "/"

    def derive(self, hex: str):
        return Payload(
            urljoin(self.url, "derive"),
            {**sc.network_identifier(self.network), **sc.public_key(hex)},
        )

    def balances(self, address: str, **at_state_identifier):
        return Payload(
            urljoin(self.url, "balances"),
            {
                **sc.network_identifier(self.network),
                **sc.account_identifier(address),
                **sc.at_state_identifier(**at_state_identifier),
            },
        )

    def stakes(self, address: str, **at_state_identifier):
        return Payload(
            urljoin(self.url, "stakes"),
            {
                **sc.network_identifier(self.network),
                **sc.account_identifier(address),
                **sc.at_state_identifier(**at_state_identifier),
            },
        )

    def unstakes(self, address: str, **at_state_identifier):
        return Payload(
            urljoin(self.url, "unstakes"),
            {
                **sc.network_identifier(self.network),
                **sc.account_identifier(address),
                **sc.at_state_identifier(**at_state_identifier),
            },
        )

    def transactions(
        self, address: str, cursor: str, limit: int, **at_state_identifier
    ):
        assert limit < 31
        return Payload(
            urljoin(self.url, "transactions"),
            {
                **sc.network_identifier(self.network),
                **sc.account_identifier(address),
                **sc.at_state_identifier(**at_state_identifier),
                "cursor": cursor,
                "limit": limit,
            },
        )


class GatewayValidatorPayloads:
    def __init__(self, network: str, url: str):
        self.network = network
        self.url = urljoin(url, "validator/")
        assert self.url[-1] == "/"

    def derive(self, hex: str):
        return Payload(
            urljoin(self.url, "derive"),
            {
                **sc.network_identifier(self.network),
                **sc.public_key(hex),
            },
        )

    def __call__(self, address: str, **at_state_identifier):
        return Payload(
            self.url,
            {
                **sc.network_identifier(self.network),
                **sc.validator_identifier(address)
                ** sc.at_state_identifier(**at_state_identifier),
            },
        )


class GatewayTransactionPayloads:
    def __init__(self, network: str, url: str):
        self.network = network
        self.url = urljoin(url, "transaction/")
        assert self.url[-1] == "/"

    def rules(self, **at_state_identifier):
        return Payload(
            urljoin(self.url, "rules"),
            {
                **sc.network_identifier(self.network),
                **sc.at_state_identifier(**at_state_identifier),
            },
        )

    def build(
        self,
        actions: list[dict],
        fee_payer_address: str,
        message: str,
        disable_token_mint_and_burn: bool,
        **at_state_identifier,
    ):

        if not isinstance(actions, list):
            actions = list(actions)

        return Payload(
            urljoin(self.url, "build"),
            {
                **sc.network_identifier(self.network),
                **sc.at_state_identifier(**at_state_identifier),
                "actions": actions,
                **sc.fee_payer(fee_payer_address),
                "message": message,
                "disable_token_mint_and_burn": disable_token_mint_and_burn,
            },
        )

    def finalize(self, unsigned_transaction: str, hex: str, bytes: str, submit: bool):
        return Payload(
            urljoin(self.url, "finalize"),
            {
                **sc.network_identifier(self.network),
                "unsigned_transaction": unsigned_transaction,
                **sc.signiture(hex, bytes),
                "submit": submit,
            },
        )

    def submit(self, signed_transaction: str):
        return Payload(
            urljoin(self.url, "submit"),
            {
                **sc.network_identifier(self.network),
                "signed_transaction": signed_transaction,
            },
        )

    def status(self, hash: str, **at_state_identifier):
        return Payload(
            urljoin(self.url, "status"),
            {
                **sc.network_identifier(self.network),
                **sc.transaction_identifier(hash),
                **sc.at_state_identifier(**at_state_identifier),
            },
        )


class RadixGateway:
    def __init__(self, network: str = None, base_url: str = None):

        self.network = network
        if network is None:
            self.network = "mainnet"

        self.base_url = base_url
        if base_url is None:
            self.base_url = "https://mainnet-gateway.radixdlt.com"

    def gateway(self):
        return Payload(url=urljoin(self.base_url, "gateway"), payload=dict())

    def validators(self, **at_state_identifier):
        return Payload(
            url=urljoin(self.base_url, "validators"),
            payload={
                **sc.network_identifier(self.network),
                **sc.at_state_identifier(**at_state_identifier),
            },
        )

    @property
    def account(self):
        return GatewayAccountPayloads(network=self.network, url=self.base_url)

    @property
    def token(self):
        return GatewayTokenPayloads(network=self.network, url=self.base_url)

    @property
    def validator(self):
        return GatewayValidatorPayloads(network=self.network, url=self.base_url)

    @property
    def transaction(self):
        return GatewayTransactionPayloads(network=self.network, url=self.base_url)


if __name__ == "__main__":

    hex = "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"
    wallet = "rdx1qsp9yzlpkvzs2dzkd56zpftr3jkp4mxz8d8r6nnqy26202mhnu7zpmgephkav"
    rri = "caviar_rr1qvnxng85y762xs3fklvxmequaww8k0nhraqv7nqjvmxs4ahu3d"

    # ga = GatewayAccountPayloads(
    #     network="mainnet", url="https://mainnet-gateway.radixdlt.com"
    # )
    # payloadObj = ga.derive(hex=hex)
    # payloadObj = ga.stakes(address=wallet)
    # payloadObj = ga.unstakes(address=wallet)
    # payloadObj = ga.balances(address=wallet)
    # payloadObj = ga.transactions(address=wallet, cursor="0", limit=2)

    # gtp = GatewayTokenPayloads(
    #     network="mainnet", url="https://mainnet-gateway.radixdlt.com"
    # )
    # payloadObj = gtp.native()
    # payloadObj = gtp(rri)

    rgw = RadixGateway()
    # payloadObj = rgw.gateway()
    payloadObj = rgw.account.derive(hex)
    payloadObj = rgw.token(rri)
    payloadObj = rgw.token.native()

    print(payloadObj)

    # resp = post_payload(url=payloadObj.url, payload=payloadObj.payload)
    # print(resp)
