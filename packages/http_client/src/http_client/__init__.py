from concurrent.futures import ThreadPoolExecutor
from os import getenv, replace, unlink
from os.path import dirname
from tempfile import NamedTemporaryFile
from time import perf_counter_ns
from typing import Any
from urllib.error import HTTPError

from httpx import (
    AsyncClient,
    AsyncHTTPTransport,
    Client,
    HTTPStatusError,
    HTTPTransport,
    Limits,
)
from httpx._types import HeaderTypes
from loguru import logger

PLAY_LOGGER_LOCATION = "G:\\Projects\\monorepo\\logs\\play.log"
LIMITER = Limits(max_connections=100, max_keepalive_connections=5, keepalive_expiry=30)
ASYNC_TRANSPORT = AsyncHTTPTransport(http2=True, limits=LIMITER)
SYNC_TRANSPORT = HTTPTransport(http2=True, limits=LIMITER)
BUNGIE_API_KEY: str = str(getenv("BUNGIE_API_KEY"))
TRANSPORT_HEADERS: HeaderTypes = {"X-API-KEY": BUNGIE_API_KEY}


try:
    unlink(PLAY_LOGGER_LOCATION)
except NotImplementedError as unlink_error:
    logger.error(unlink_error)

logger.add(PLAY_LOGGER_LOCATION, enqueue=True, serialize=True)


def format_duration(value: int, decimals: int = 2) -> str:
    """
    Convert a duration from nanoseconds into the largest readable time unit.

    Examples:
        >>> format_duration(500)
        '500 ns'

        >>> format_duration(1_500)
        '1.5 μs'

        >>> format_duration(1_500_000)
        '1.5 ms'

        >>> format_duration(1_500_000_000)
        '1.5 s'

        >>> format_duration(90_000_000_000)
        '1.5 min'

        >>> format_duration(5_400_000_000_000)
        '1.5 hr'

    Args:
        value:
            Duration in nanoseconds.

        decimals:
            Maximum number of decimal places to display.

    Returns:
        A human-readable duration string.
    """

    if value < 0:
        raise ValueError("Duration must be non-negative")

    units = [
        ("ns", 1),
        ("μs", 1_000),
        ("ms", 1_000_000),
        ("s", 1_000_000_000),
        ("min", 60 * 1_000_000_000),
        ("hr", 60 * 60 * 1_000_000_000),
    ]

    size = float(value)
    unit_name = "ns"

    for name, factor in units:
        if value >= factor:
            unit_name = name
            size = value / factor

    formatted = f"{size:.{decimals}f}".rstrip("0").rstrip(".")

    return f"{formatted} {unit_name}"


async def download_async(client: AsyncClient, url: str, output_path: str) -> None:
    try:
        pass
    except HTTPError as error:
        print(error)
    finally:
        pass


def download_sync(
    url: str,
    output_path: str,
    file_suffix: str,
    client: Client,
) -> None:
    """Download a resource synchronously to a file.

    The response is streamed in chunks and written to a temporary file
    located in the destination directory. Once the download completes
    successfully, the temporary file is atomically moved to the requested
    output path.

    Args:
        url: URL or client-relative path of the resource to download.
        output_path: Destination path for the downloaded file.
        file_suffix: Suffix to use when creating the temporary file.
        client: HTTPX client used to perform the request.

    Raises:
        HTTPStatusError: If the server returns an unsuccessful HTTP status.
        FileNotFoundError: If the destination directory or file cannot be
            accessed.

    Returns:
        None.
    """
    __dirname = dirname(output_path)
    temp_file_name: str = ""
    chunk_count = 0
    total_size = 0

    start_time = perf_counter_ns()
    try:
        with NamedTemporaryFile(
            suffix=file_suffix,
            mode="wb",
            delete=False,
            delete_on_close=False,
            dir=__dirname,
        ) as tmp_file_desc:
            temp_file_name: str = tmp_file_desc.name
            logger.debug("Created Tempfile: {}", temp_file_name)
            with client.stream("GET", url) as response:
                response.raise_for_status()
                for chunk in response.iter_bytes(chunk_size=1000 * 256):
                    if not chunk:
                        continue
                    tmp_file_desc.write(chunk)
                    total_size += len(chunk)
                    chunk_count += 1
            tmp_file_desc.flush()
            logger.debug("Flushed Tempfile: {}", temp_file_name)
    except (HTTPError, FileNotFoundError, HTTPStatusError) as error:
        logger.error(error)
        if temp_file_name != "":
            unlink(temp_file_name)
        return

    if temp_file_name != "":
        raise RuntimeError("Temporary file was not created")

    replace(temp_file_name, output_path)
    stop_endtime = perf_counter_ns()
    logger.debug("Renamed Tempfile {} to {}", temp_file_name, output_path)
    logger.info(
        "Downloaded File: {} {total_size} bytes {chunk_count} chunks {elapsed_time}",
        output_path,
        total_size=total_size,
        chunk_count=chunk_count,
        elapsed_time=(format_duration(stop_endtime - start_time)),
    )


def download_all_sync(all_urls: list[list[Any]]) -> None:
    """Download multiple resources concurrently using a shared HTTP client.

    Creates a single synchronous HTTPX client and uses a thread pool to
    download all resources in parallel. Each download is delegated to
    ``download_sync``.

    Args:
        all_urls: A list of argument sequences containing the parameters
            required by ``download_sync``, excluding the HTTP client.
            Each element should contain ``url``, ``output_path``, and
            ``file_suffix``.

    Returns:
        None.
    """

    with Client(
        transport=SYNC_TRANSPORT,
        headers=TRANSPORT_HEADERS,
        base_url="https://www.bungie.net",
    ) as client:
        url_list: list[list[Any]] = [[*x, client] for x in all_urls]

        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(lambda p: download_sync(*p), url_list)  # type: ignore


def main() -> None:
    print("Hello from http-client!")
