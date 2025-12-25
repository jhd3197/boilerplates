"""API mixin for myproject.

This module provides HTTP API client functionality.
"""

import os
from typing import Any, Dict, Optional

from ..types import Result


class APIMixin:
    """Mixin class for API operations.

    Provides HTTP request functionality and API interaction.
    Uses cooperative multiple inheritance pattern with super().

    Attributes:
        api_base_url: Base URL for API requests
        api_key: API authentication key
        api_timeout: Request timeout in seconds
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the API mixin.

        Args:
            *args: Positional arguments passed to super()
            **kwargs: Keyword arguments passed to super()
        """
        super().__init__(*args, **kwargs)

        # Get API settings from config or environment
        self.api_base_url = kwargs.get('api_base_url') or os.getenv('API_BASE_URL', '')
        self.api_key = kwargs.get('api_key') or os.getenv('API_KEY')
        self.api_timeout = kwargs.get('api_timeout', 30)

        if hasattr(self, 'config'):
            if self.config.api_key:
                self.api_key = self.config.api_key
            self.api_timeout = self.config.timeout

    def _get_headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Build request headers.

        Args:
            extra_headers: Additional headers to include

        Returns:
            Dictionary of headers
        """
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "MyProject-Client/1.0",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Result:
        """Make a GET request.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Result dictionary with API response
        """
        try:
            url = f"{self.api_base_url}{endpoint}"
            headers = self._get_headers()

            # In a real implementation, you'd use requests or httpx
            # For this boilerplate, we simulate the request
            return {
                "success": True,
                "data": {
                    "method": "GET",
                    "url": url,
                    "params": params or {},
                    "response": {"simulated": True},
                },
                "metadata": {
                    "status_code": 200,
                    "headers": headers,
                    "timeout": self.api_timeout,
                },
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"GET request failed: {str(e)}",
                "data": None,
            }

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Result:
        """Make a POST request.

        Args:
            endpoint: API endpoint path
            data: Form data
            json_data: JSON data

        Returns:
            Result dictionary with API response
        """
        try:
            url = f"{self.api_base_url}{endpoint}"
            headers = self._get_headers()

            return {
                "success": True,
                "data": {
                    "method": "POST",
                    "url": url,
                    "data": data,
                    "json": json_data,
                    "response": {"simulated": True, "id": "12345"},
                },
                "metadata": {
                    "status_code": 201,
                    "headers": headers,
                },
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"POST request failed: {str(e)}",
                "data": None,
            }

    def put(self, endpoint: str, data: Dict[str, Any]) -> Result:
        """Make a PUT request.

        Args:
            endpoint: API endpoint path
            data: Data to send

        Returns:
            Result dictionary with API response
        """
        try:
            url = f"{self.api_base_url}{endpoint}"
            headers = self._get_headers()

            return {
                "success": True,
                "data": {
                    "method": "PUT",
                    "url": url,
                    "data": data,
                    "response": {"simulated": True, "updated": True},
                },
                "metadata": {
                    "status_code": 200,
                    "headers": headers,
                },
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"PUT request failed: {str(e)}",
                "data": None,
            }

    def delete(self, endpoint: str) -> Result:
        """Make a DELETE request.

        Args:
            endpoint: API endpoint path

        Returns:
            Result dictionary with API response
        """
        try:
            url = f"{self.api_base_url}{endpoint}"
            headers = self._get_headers()

            return {
                "success": True,
                "data": {
                    "method": "DELETE",
                    "url": url,
                    "response": {"simulated": True, "deleted": True},
                },
                "metadata": {
                    "status_code": 204,
                    "headers": headers,
                },
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"DELETE request failed: {str(e)}",
                "data": None,
            }

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> Result:
        """Make a generic HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            Result dictionary with API response
        """
        method = method.upper()

        if method == "GET":
            return self.get(endpoint, kwargs.get('params'))
        elif method == "POST":
            return self.post(endpoint, kwargs.get('data'), kwargs.get('json'))
        elif method == "PUT":
            return self.put(endpoint, kwargs.get('data', {}))
        elif method == "DELETE":
            return self.delete(endpoint)
        else:
            return {
                "success": False,
                "error": f"Unsupported HTTP method: {method}",
                "data": None,
            }
