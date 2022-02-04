### A Radix python Api module

A python module to speed up the json payload construction for calling the Radix DLT core and gateway API.

https://docs.radixdlt.com/main/apis/api-specification.html

### Gateway endpoints / methods (version 1.0.0)
- gateway()
- account - not callable, just a property
    - derive()
    - balances()
    - stake()
    - unstake()
    - transactions()
- token()
    - native()
    - derive()
- validator()
    - derive()
- validators()
- transaction - not callable, just a property
    - rules()
    - build()
    - finalize()
    - submit()
    - status()



### Quick example usage
import the main things we will need

    from pyradapi.core import RadixGateway, post_payload_object, Action

create a gateway object

    rgw = RadixGateway()

To access accounts:

    rgw.account

Then any endpoint:

    payloadObj = rgw.account.stakes(wallet_address)

This will return an Payload Object which has 2 attributes

 - url:		https://mainnet-gateway.radixdlt.com/account/stakes 
 - payload:	{"network_identifier": {"network": "mainnet"}, "account_identifier": {"address": "rdx1qsp4xutv3p3fnvmnzheag9dvvxmy9ajmplth25tlx0dnj2dg3sptjyssltfq8"}}


This then can be passed to the post_payload_object() function to get a response:

    resp = post_payload_object(payloadObj)



