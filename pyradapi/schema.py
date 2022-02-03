def network_identifier(network: str) -> dict:
    return {"network_identifier": {"network": network}}


def _address_builder(name: str, address: str) -> dict:
    return {name: {"address": address}}


def account_identifier(address: str) -> dict:
    return _address_builder("account_identifier", address)


def validator_identifier(address: str) -> dict:
    return _address_builder("validator_identifier", address)


def to_account(address: str) -> dict:
    return _address_builder("to_account", address)


def from_account(address: str) -> dict:
    return _address_builder("from_account", address)


def to_validator(address: str) -> dict:
    return _address_builder("to_validator", address)


def from_validator(address: str) -> dict:
    return _address_builder("from_validator", address)


def fee_payer(address: str) -> dict:
    return _address_builder("fee_payer", address)


def token_identifier(rri: str) -> dict:
    return {"token_identifier": {"rri": rri}}


def public_key(hex: str) -> dict:
    return {"public_key": {"hex": hex}}


def amount(value: str, rri: str) -> dict:
    return {"amount": {"value": value, **token_identifier(rri)}}


def token_supply(value: str, rri: str) -> dict:
    return {"token_supply": {"value": value, **token_identifier(rri)}}


def signature(hex: str, bytes: str) -> dict:
    return {"signature": {**public_key(hex), "bytes": bytes}}


def transaction_identifier(hash: str) -> dict:
    return {"transaction_identifier": {"hash": hash}}


def token_properties(
    name: str,
    description: str,
    icon_url: str,
    url: str,
    symbol: str,
    is_supply_mutable: bool,
    granularity: str,
    owner_address: str,
) -> dict:
    return {
        "token_properties": {
            "name": name,
            "description": description,
            "icon_url": icon_url,
            "url": url,
            "symbol": symbol,
            "is_supply_mutable": is_supply_mutable,
            "granularity": granularity,
            **_address_builder("owner", owner_address),
        }
    }


class Action:
    def CreateTokenDefinition(
        name: str,
        description: str,
        icon_url: str,
        url: str,
        symbol: str,
        is_supply_mutable: bool,
        granularity: str,
        owner_address: str,
        value: str,
        rri: str,
        to_account_address: str,
    ):
        return {
            "type": "CreateTokenDefinition",
            **token_properties(
                name,
                description,
                icon_url,
                url,
                symbol,
                is_supply_mutable,
                granularity,
                owner_address,
            ),
            **token_supply(value, rri),
            **to_account(to_account_address),
        }

    def TransferTokens(
        from_account_address: str, to_account_address: str, value: str, rri: str
    ):
        return {
            "type": "TransferTokens",
            **from_account(from_account_address),
            **to_account(to_account_address),
            **amount(value, rri),
        }

    def StakeTokens(
        from_account_address: str, to_validator_address: str, value: str, rri: str
    ):
        return {
            "type": "StakeTokens",
            **from_account(from_account_address),
            **to_validator(to_validator_address),
            **amount(value, rri),
        }

    def UnstakeTokens(
        from_validator_address: str,
        to_account_address: str,
        value: str,
        rri: str,
        unstake_percentage: float,
    ):
        assert (unstake_percentage > 1) and (unstake_percentage <= 100)
        return {
            "type": "UnstakeTokens",
            **from_validator(from_validator_address),
            **to_account(to_account_address),
            **amount(value, rri),
            "unstake_percentage": unstake_percentage,
        }

    def MintTokens(address: str, value: str, rri: str):
        return {"type": "MintTokens", **to_account(address), **amount(value, rri)}

    def BurnTokens(address: str, value: str, rri: str):
        return {"type": "BurnTokens", **from_account(address), **amount(value, rri)}


def at_state_identifier(
    version: int = None,
    timestamp: str = None,
    epoch: int = None,
    round: int = None,
    **kwargs
) -> dict:
    temp = dict()
    if version:
        temp["version"] = version
    if timestamp:
        temp["timestamp"] = timestamp
    if epoch:
        temp["epoch"] = epoch
    if round:
        temp["round"] = round
    if len(temp) > 0:
        return {"at_state_identifier": temp}
    return {}
