import requests
import json
from typing import Dict, List, Optional

class AffirmationsAPI:
    def __init__(self):
        self.base_url = "https://www.affirmations.dev"
    
    def get_random_affirmation(self) -> Dict:
        """Obtiene una afirmación aleatoria de la API"""
        try:
            response = requests.get(f"{self.base_url}/affirmation")
            if response.status_code == 200:
                return response.json()
            return {"affirmation": "Soy capaz de lograr todo lo que me propongo"}
        except Exception as e:
            print(f"Error al obtener afirmación: {e}")
            return {"affirmation": "Soy capaz de lograr todo lo que me propongo"}
    
    def get_multiple_affirmations(self, count: int = 5) -> List[Dict]:
        """Obtiene múltiples afirmaciones aleatorias"""
        try:
            response = requests.get(f"{self.base_url}/affirmations", params={"count": count})
            if response.status_code == 200:
                return response.json()
            return [{"affirmation": "Soy capaz de lograr todo lo que me propongo"}]
        except Exception as e:
            print(f"Error al obtener afirmaciones: {e}")
            return [{"affirmation": "Soy capaz de lograr todo lo que me propongo"}]

# Instancia global de la API
affirmations_api = AffirmationsAPI() 