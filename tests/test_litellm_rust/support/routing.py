from collections.abc import Generator
from contextlib import contextmanager

from litellm.rust_bridge import runtime
from litellm.rust_bridge.catalog import Route
from litellm.rust_bridge.configuration import Decision
from tests.test_litellm_rust.support.recording_server import RecordingServer


@contextmanager
def native_route(*routes: Route) -> Generator[None]:
    with runtime.pinned(Decision.RUST_REQUIRED, *routes):
        yield


def assert_served_natively(server: RecordingServer, count: int = 1) -> None:
    assert len(server.requests) == count
    assert not any(request.headers.get("user-agent", "").startswith("python-httpx") for request in server.requests)
