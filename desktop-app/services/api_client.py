"""API client for communicating with the Django backend."""

import requests
from utils.config import API_BASE_URL


class ApiClient:
    """Client for making API requests to the backend."""
    
    def __init__(self):
        self.token = None
        self.session = requests.Session()
    
    def set_token(self, token: str):
        """Set the authentication token."""
        self.token = token
        self.session.headers.update({"Authorization": f"Token {token}"})
    
    def clear_token(self):
        """Clear the authentication token."""
        self.token = None
        self.session.headers.pop("Authorization", None)
    
    def register(self, username: str, email: str, password: str) -> dict:
        """Register a new user."""
        response = self.session.post(
            f"{API_BASE_URL}/auth/register/",
            json={
                "username": username,
                "email": email,
                "password": password,
                "password_confirm": password,
            }
        )
        response.raise_for_status()
        data = response.json()
        self.set_token(data["token"])
        return data
    
    def login(self, username: str, password: str) -> dict:
        """Login and get auth token."""
        response = self.session.post(
            f"{API_BASE_URL}/auth/login/",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.set_token(data["token"])
        return data
    
    def logout(self):
        """Logout and clear token."""
        try:
            self.session.post(f"{API_BASE_URL}/auth/logout/")
        except Exception:
            pass
        self.clear_token()
    
    def upload_csv(self, file_path: str) -> dict:
        """Upload a CSV file."""
        with open(file_path, "rb") as f:
            response = self.session.post(
                f"{API_BASE_URL}/upload/",
                files={"file": f}
            )
        response.raise_for_status()
        return response.json()
    
    def get_datasets(self) -> list:
        """Get list of user's datasets."""
        response = self.session.get(f"{API_BASE_URL}/datasets/")
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id: int) -> dict:
        """Get dataset details."""
        response = self.session.get(f"{API_BASE_URL}/datasets/{dataset_id}/")
        response.raise_for_status()
        return response.json()
    
    def get_summary(self, dataset_id: int) -> dict:
        """Get dataset summary statistics."""
        response = self.session.get(f"{API_BASE_URL}/datasets/{dataset_id}/summary/")
        response.raise_for_status()
        return response.json()
    
    def download_report(self, dataset_id: int, save_path: str):
        """Download PDF report for a dataset."""
        response = self.session.get(
            f"{API_BASE_URL}/datasets/{dataset_id}/report/",
            stream=True
        )
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


api_client = ApiClient()
