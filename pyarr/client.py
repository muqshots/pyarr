from typing import Any, Type, Union

from aiohttp import ClientSession, TCPConnector

from pyarr.config import ConfigSchema
from pyarr.exceptions import MissingClientAuthentication
from pyarr.request import Response
from pyarr.utils import get_url


class Client:
    """Client for communicating with Sonarr / Radarr
    Parses client config and provides a ClientSession factory.
    Args:
        platform: sonarr or radarr
        address: Instance TCP address
        api_key: API Key
        use_ssl: Whether to use SSL
        verify_ssl: Whether to verify SSL certificates
        pool_size: Connection pool size
        response_cls: Custom Response class
    Attributes:
        config: Client configuration object
    """

    def __init__(
        self,
        platform: str,
        address: Union[str, bytes],
        api_key: str,
        use_ssl: bool = True,
        verify_ssl: bool = None,
        pool_size: int = 100,
        response_cls: Type[Response] = None,
        session_cls: Type[ClientSession] = None,
    ):
        if self.platform:
            self._api_key = self.config.session.api_key  # type: ignore
        else:
            raise MissingClientAuthentication(
                "No known authentication methods provided"
            )
        # Load config
        self.config = ConfigSchema(many=False).load(
            dict(
                address=address,
                session=dict(
                    api_key=api_key,
                    use_ssl=use_ssl or True,
                    verify_ssl=verify_ssl or True,
                ),
            )
        )

        if self.config.session.api_key:
            self._api_key = self.config.session.api_key  # type: ignore
        else:
            raise MissingClientAuthentication(
                "No known authentication methods provided"
            )

        if session_cls and not issubclass(session_cls, ClientSession):
            raise TypeError(
                f"Client :session: ({session_cls}) is not of {ClientSession} type"
            )
        if response_cls and not issubclass(response_cls, Response):
            raise TypeError(
                f"Client :response_cls: ({response_cls}) is not of {Response} type"
            )

        self.session_cls = session_cls or ClientSession
        self.response_cls = response_cls or Response
        self.base_url = get_url(str(self.config.address), bool(use_ssl))
        self.pool_size = pool_size

    def get_session(self) -> Any:
        connector_args = dict(limit=self.pool_size)  # type: Any

        if self.config.session.use_ssl:
            connector_args["verify_ssl"] = self.config.session.verify_ssl

        return self.session_cls(
            headers={"X-Api-Key": self._api_key},
            skip_auto_headers=["Content-Type"],
            response_class=self.response_cls,
            connector=TCPConnector(**connector_args),
        )
