"""Tests for ABS MCP Server."""

import pytest
from unittest.mock import Mock, patch
from abs_mcp_server.server import search_datasets, ABSAPIError


class TestSearchDatasets:
    """Test search_datasets function."""

    @patch("abs_mcp_server.server.requests.get")
    def test_search_datasets_success(self, mock_get):
        """Test successful dataset search."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "dataflows": [
                {
                    "id": "ABS_CENSUS2021_T01",
                    "name": "Census 2021 Population",
                    "description": "Population counts from 2021 Census",
                    "version": "1.0",
                    "agencyID": "ABS",
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = search_datasets("census")

        assert len(result) == 1
        assert result[0]["id"] == "ABS_CENSUS2021_T01"
        assert "census" in result[0]["name"].lower()

    @patch("abs_mcp_server.server.requests.get")
    def test_search_datasets_api_error(self, mock_get):
        """Test API error handling."""
        mock_get.side_effect = Exception("API Error")

        with pytest.raises(ABSAPIError):
            search_datasets("test")


def test_server_initialization():
    """Test that server can be imported and initialized."""
    from abs_mcp_server.server import mcp

    assert mcp.name == "abs-data"
