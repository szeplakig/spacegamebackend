import json

from sqlalchemy import LargeBinary, TypeDecorator


class BlobInt(TypeDecorator):
    """Store integers as a JSON-encoded string in a BLOB column."""

    impl = LargeBinary
    cache_ok = True

    def process_bind_param(self, value, dialect):  # noqa: ANN001, ANN201
        if value is not None:
            # Convert the integer to a JSON string and encode it to bytes
            return json.dumps(value).encode("utf-8")
        return value

    def process_result_value(self, value, dialect):  # noqa: ANN001, ANN201
        if value is not None:
            return value
        return value
