import httpx
from loguru import logger

class GeocodingService:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {"User-Agent": "CityUnderControl/1.0"}

    async def address_to_coords(self, address: str) -> dict | None:
        """Конвертирует адрес в координаты."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params={"q": address, "format": "json", "limit": 1},
                    headers=self.headers
                )
                data = response.json()
                if data:
                    return {
                        "latitude": float(data[0]["lat"]),
                        "longitude": float(data[0]["lon"]),
                        "display_name": data[0]["display_name"]
                    }
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
        return None

    async def coords_to_address(self, lat: float, lon: float) -> str | None:
        """Конвертирует координаты в адрес (reverse geocoding)."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/reverse",
                    params={"lat": lat, "lon": lon, "format": "json"},
                    headers=self.headers
                )
                data = response.json()
                return data.get("display_name")
        except Exception as e:
            logger.error(f"Reverse geocoding error: {e}")
        return None

geocoding_service = GeocodingService()