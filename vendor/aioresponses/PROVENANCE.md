# aioresponses aiohttp compatibility source

Upstream: https://github.com/pnuckowski/aioresponses

PyPI version: 0.7.9. Original source archive: https://files.pythonhosted.org/packages/28/fb/e3f08af812b3e66fca511ea1babb9dfddeca5965dea2a4d13b6926e0b1c2/aioresponses-0.7.9.tar.gz

Verified SHA256: `1dcfa28938fc006f046a98383a7c07ac180be7a492c1ed557f5cd7b0805357d3`. Original license retained. Tests are not copied or changed.

The only mock behavior patch passes `stream_writer=Mock(output_size=0)` when the current ClientResponse signature declares the new required argument. The response matching, payloads, assertions and transport mocks are unchanged. This permits the latest aiohttp required by CCXT without suppressing or weakening existing Basana tests. Retire after an upstream release adds aiohttp 3.14 support.
