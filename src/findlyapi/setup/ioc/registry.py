from collections.abc import Iterable

from dishka import Provider
from dishka.integrations.fastapi import FastapiProvider

from findlyapi.setup.ioc.providers import RequestProvider


def get_providers() -> Iterable[Provider]:
    return (
        RequestProvider(),
        FastapiProvider()
    )