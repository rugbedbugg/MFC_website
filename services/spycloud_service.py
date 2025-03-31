import requests
from flask import current_app
import logging
from typing import Dict, List, Optional

class SpyCloudService:
    def __init__(self):
        self.api_key = current_app.config['SPYCLOUD_API_KEY']
        self.api_endpoint = current_app.config['SPYCLOUD_API_ENDPOINT']
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_breach_data(self, email: str) -> List[Dict]:
        """
        Fetch breach data for a given email from SpyCloud API
        """
        try:
            endpoint = f"{self.api_endpoint}/breaches"
            params = {'email': email}
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('breaches', [])
            else:
                logging.error(f"SpyCloud API error: {response.status_code} - {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching breach data: {str(e)}")
            return []

    def get_exposure_data(self, email: str) -> Dict:
        """
        Fetch exposure data for a given email from SpyCloud API
        """
        try:
            endpoint = f"{self.api_endpoint}/exposures"
            params = {'email': email}
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"SpyCloud API error: {response.status_code} - {response.text}")
                return {}
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching exposure data: {str(e)}")
            return {} 