from urllib.parse import urljoin

import pyradapi.schema as sc
from pyradapi.payload import Payload


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

    def stakes(self, address: str, cursor: str, limit: int, **at_state_identifier):
        return Payload(
            urljoin(self.url, "stakes"),
            {
                **sc.network_identifier(self.network),
                **sc.at_state_identifier(**at_state_identifier),
                **sc.validator_identifier(address),
                "cursor": cursor,
                "limit": limit,
            },
        )

    def __call__(self, address: str, **at_state_identifier):
        return Payload(
            self.url,
            {
                **sc.network_identifier(self.network),
                **sc.validator_identifier(address),
                **sc.at_state_identifier(**at_state_identifier),
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
        actions,
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
                **sc.signature(hex, bytes),
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
    pass
