from .operation import Operation
from .utils import check_muxed_ed25519_account
from ..strkey import StrKey
from ..xdr import Xdr


class AccountMerge(Operation):
    """The :class:`AccountMerge` object, which represents a
    AccountMerge operation on Stellar's network.

    Transfers the native balance (the amount of XLM an account holds) to
    another account and removes the source account from the ledger.

    Threshold: High

    :param destination: Destination to merge the source account into.
    :param source: The source account (defaults to transaction source).

    """

    def __init__(self, destination: str, source: str = None) -> None:
        super().__init__(source)
        check_muxed_ed25519_account(destination)
        self.destination: str = destination

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.ACCOUNT_MERGE

    def _to_operation_body(self) -> Xdr.nullclass:
        destination = StrKey.decode_muxed_account(self.destination)
        body = Xdr.nullclass()
        body.type = Xdr.const.ACCOUNT_MERGE
        body.destination = destination
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "AccountMerge":
        """Creates a :class:`AccountMerge` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = StrKey.encode_muxed_account(operation_xdr_object.body.destination)

        return cls(source=source, destination=destination)
