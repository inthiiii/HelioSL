import httpx


GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)

FORECAST_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


def geocode_location(
    location: str,
) -> tuple[float, float] | None:

    response = httpx.get(
        GEOCODING_URL,
        params={
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("results", [])

    if not results:
        return None

    result = results[0]

    return (
        result["latitude"],
        result["longitude"],
    )


def get_weather_context(
    location: str,
) -> dict:

    coordinates = geocode_location(
        location
    )

    if not coordinates:
        return {
            "available": False,
            "reason": "Location not found",
        }

    latitude, longitude = coordinates

    response = httpx.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "cloud_cover,"
                "precipitation,"
                "weather_code"
            ),
            "daily": (
                "shortwave_radiation_sum,"
                "precipitation_sum"
            ),
            "timezone": "auto",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    current = data.get(
        "current",
        {},
    )

    daily = data.get(
        "daily",
        {},
    )

    return {
        "available": True,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "temperature_c":
            current.get(
                "temperature_2m"
            ),
        "humidity_percent":
            current.get(
                "relative_humidity_2m"
            ),
        "cloud_cover_percent":
            current.get(
                "cloud_cover"
            ),
        "precipitation_mm":
            current.get(
                "precipitation"
            ),
        "weather_code":
            current.get(
                "weather_code"
            ),
        "shortwave_radiation_sum":
            (
                daily.get(
                    "shortwave_radiation_sum",
                    [None],
                )[0]
                if daily
                else None
            ),
    }