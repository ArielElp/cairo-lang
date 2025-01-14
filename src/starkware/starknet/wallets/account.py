import dataclasses
from abc import ABC, abstractmethod
from typing import Awaitable, Callable, List, Tuple

from starkware.starknet.services.api.contract_class import ContractClass
from starkware.starknet.wallets.starknet_context import StarknetContext

DEFAULT_ACCOUNT_DIR = "~/.starknet_accounts"


@dataclasses.dataclass
class WrappedMethod:
    address: int
    selector: int
    calldata: List[int]
    max_fee: int
    signature: List[int]
    nonce: int


class Account(ABC):
    @classmethod
    @abstractmethod
    async def create(cls, starknet_context: StarknetContext, account_name: str) -> "Account":
        """
        Constructs an instance of the class.
        """

    @abstractmethod
    async def deploy(self):
        """
        Initializes the account. For example, this may include choosing a new random private key
        and deploying the account contract to the network.
        """

    @abstractmethod
    async def sign_invoke_transaction(
        self,
        contract_address: int,
        selector: int,
        calldata: List[int],
        chain_id: int,
        max_fee: int,
        version: int,
        nonce_callback: Callable[[int], Awaitable[int]],
        dry_run: bool = False,
    ) -> WrappedMethod:
        """
        Given a transaction to execute (or call) within the context of the account,
        prepares the required information for invoking it through the account contract.
        nonce is the nonce to be used in the transaction. If not specified, the current nonce
        is queried from the StarkNet system.
        """

    @abstractmethod
    async def deploy_contract(
        self,
        class_hash: int,
        salt: int,
        constructor_calldata: List[int],
        deploy_from_zero: bool,
        chain_id: int,
        max_fee: int,
        version: int,
        nonce_callback: Callable[[int], Awaitable[int]],
    ) -> Tuple[WrappedMethod, int]:
        """
        Prepares the required information for invoking a contract deployment function through
        the account contract.
        Returns the wrapped method and the deployed contract address.
        """

    @abstractmethod
    async def declare(
        self,
        contract_class: ContractClass,
        chain_id: int,
        max_fee: int,
        version: int,
        nonce_callback: Callable[[int], Awaitable[int]],
        dry_run: bool = False,
    ) -> WrappedMethod:
        """
        Prepares the required information for declaring a contract class through the account
        contract.
        """
