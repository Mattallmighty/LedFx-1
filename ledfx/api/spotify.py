from ledfx.config import save_config
from ledfx.api import RestEndpoint
from aiohttp import web
import logging
import json

_LOGGER = logging.getLogger(__name__)

class SpotifyEndpoint(RestEndpoint):

    ENDPOINT_PATH = "/api/spotify"

    async def get(self) -> web.Response:
        response = self._ledfx.config.get('spotify')

        return web.Response(text=json.dumps(response), status=200)

    async def put(self, request) -> web.Response:
        spotify = self._ledfx.config.get('spotify')
        if spotify is None:
            response = { 'not found': 404 }
            return web.Response(text=json.dumps(response), status=404)

        data = await request.json()
        enable_spotify = data.get('spotify_enabled')
        if enable_spotify is None:
            response = { 'status' : 'failed', 'reason': 'Required attribute "enable" was not provided' }
            return web.Response(text=json.dumps(response), status=500)


        # Update and save the configuration
        self._ledfx.config['spotify'] = enable_spotify

        save_config(
            config = self._ledfx.config, 
            config_dir = self._ledfx.config_dir)

        response = { 'status' : 'success', 'spotify_enabled' : enable_spotify}
        return web.Response(text=json.dumps(response), status=200)