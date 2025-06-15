import json
from datetime import datetime
import os
from utils.affirmations_api import affirmations_api

class DailyAffirmation:
    def __init__(self):
        self.affirmation_file = "data/daily_affirmation.json"
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Asegura que el directorio de datos existe"""
        os.makedirs("data", exist_ok=True)
    
    def _get_today_date(self):
        """Retorna la fecha de hoy en formato YYYY-MM-DD"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_daily_affirmation(self):
        """Obtiene la afirmación del día"""
        today = self._get_today_date()
        
        # Intentar cargar la afirmación del día
        if os.path.exists(self.affirmation_file):
            with open(self.affirmation_file, 'r') as f:
                data = json.load(f)
                if data.get('date') == today:
                    return data.get('affirmation')
        
        # Si no existe o es de otro día, obtener una nueva
        affirmation = affirmations_api.get_random_affirmation()
        
        # Guardar la nueva afirmación
        with open(self.affirmation_file, 'w') as f:
            json.dump({
                'date': today,
                'affirmation': affirmation
            }, f)
        
        return affirmation
    
    def save_vote(self, user_name, vote):
        """Guarda el voto de un usuario"""
        today = self._get_today_date()
        votes_file = f"data/votes_{today}.json"
        
        # Cargar votos existentes o crear nuevo archivo
        if os.path.exists(votes_file):
            with open(votes_file, 'r') as f:
                votes = json.load(f)
        else:
            votes = []
        
        # Agregar nuevo voto
        votes.append({
            'user_name': user_name,
            'vote': vote,
            'timestamp': datetime.now().isoformat()
        })
        
        # Guardar votos
        with open(votes_file, 'w') as f:
            json.dump(votes, f)
    
    def get_today_votes(self):
        """Obtiene los votos del día"""
        today = self._get_today_date()
        votes_file = f"data/votes_{today}.json"
        
        if os.path.exists(votes_file):
            with open(votes_file, 'r') as f:
                return json.load(f)
        return []

# Instancia global
daily_affirmation = DailyAffirmation() 