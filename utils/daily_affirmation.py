import json
from datetime import datetime, timedelta
import os
import random
import pytz
import calendar
from typing import Dict, List, Optional
from collections import deque

class DailyAffirmation:
    def __init__(self):
        self.affirmation_file = "data/daily_affirmation.json"
        self.recent_affirmations_file = "data/recent_affirmations.json"
        self.local_affirmations_file = "data/affirmations.json"
        self.timezone = pytz.timezone('America/Santiago')  # Zona horaria de Chile
        self.max_history = 4  # Número máximo de días a recordar
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Asegura que el directorio de datos existe"""
        os.makedirs("data", exist_ok=True)
    
    def _get_today_date(self) -> str:
        """Retorna la fecha de hoy en formato YYYY-MM-DD en la zona horaria configurada"""
        return datetime.now(self.timezone).strftime("%Y-%m-%d")
    
    def _get_current_time(self) -> datetime:
        """Retorna la hora actual en la zona horaria configurada"""
        return datetime.now(self.timezone)
    
    def _is_new_day(self, stored_date: str) -> bool:
        """Verifica si la fecha almacenada es de un día anterior"""
        today = self._get_today_date()
        return stored_date != today
    
    def _get_day_name(self) -> str:
        """Retorna el nombre del día actual en español"""
        days = {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo"
        }
        return days[datetime.now(self.timezone).weekday()]
    
    def _get_month_name(self) -> str:
        """Retorna el nombre del mes actual en español"""
        months = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre"
        }
        return months[datetime.now(self.timezone).month]
    
    def _load_affirmation_history(self) -> deque:
        """Carga el historial de afirmaciones como una pila"""
        if os.path.exists(self.recent_affirmations_file):
            with open(self.recent_affirmations_file, 'r') as f:
                history = json.load(f)
                # Convertir a deque y limitar al tamaño máximo
                return deque(history[-self.max_history:], maxlen=self.max_history)
        return deque(maxlen=self.max_history)
    
    def _save_affirmation_history(self, history: deque):
        """Guarda el historial de afirmaciones"""
        with open(self.recent_affirmations_file, 'w') as f:
            json.dump(list(history), f, ensure_ascii=False, indent=2)
    
    def _load_local_affirmations(self) -> List[str]:
        """Carga las afirmaciones locales"""
        if os.path.exists(self.local_affirmations_file):
            with open(self.local_affirmations_file, 'r') as f:
                data = json.load(f)
                return data.get('affirmations', [])
        return []
    
    def _is_affirmation_in_history(self, affirmation: str, history: deque) -> bool:
        """Verifica si una afirmación está en el historial"""
        return any(entry['affirmation'] == affirmation for entry in history)
    
    def get_daily_affirmation(self) -> Dict:
        """Obtiene la afirmación del día"""
        today = self._get_today_date()
        
        # Intentar cargar la afirmación del día
        if os.path.exists(self.affirmation_file):
            with open(self.affirmation_file, 'r') as f:
                data = json.load(f)
                if not self._is_new_day(data.get('date', '')):
                    return data.get('affirmation')
        
        # Si no existe o es de otro día, obtener una nueva
        local_affirmations = self._load_local_affirmations()
        if not local_affirmations:
            return {"affirmation": "Soy capaz de lograr todo lo que me propongo"}
        
        # Cargar historial actual
        history = self._load_affirmation_history()
        
        # Intentar encontrar una afirmación que no esté en el historial
        max_attempts = min(10, len(local_affirmations))
        attempts = 0
        while attempts < max_attempts:
            affirmation = random.choice(local_affirmations)
            if not self._is_affirmation_in_history(affirmation, history):
                # Crear nueva entrada para el historial
                new_entry = {
                    'date': today,
                    'day_name': self._get_day_name(),
                    'month_name': self._get_month_name(),
                    'affirmation': affirmation,
                    'timestamp': self._get_current_time().isoformat()
                }
                
                # Agregar al historial (la pila se encargará de mantener el tamaño máximo)
                history.append(new_entry)
                
                # Guardar el historial actualizado
                self._save_affirmation_history(history)
                
                # Guardar la afirmación del día
                with open(self.affirmation_file, 'w') as f:
                    json.dump({
                        'date': today,
                        'day_name': self._get_day_name(),
                        'month_name': self._get_month_name(),
                        'affirmation': {"affirmation": affirmation},
                        'timestamp': self._get_current_time().isoformat()
                    }, f, ensure_ascii=False, indent=2)
                
                return {"affirmation": affirmation}
            attempts += 1
        
        # Si no se pudo encontrar una afirmación nueva, usar una aleatoria
        affirmation = random.choice(local_affirmations)
        return {"affirmation": affirmation}
    
    def save_vote(self, user_name: str, vote: str):
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
            'timestamp': self._get_current_time().isoformat(),
            'day_name': self._get_day_name(),
            'month_name': self._get_month_name()
        })
        
        # Guardar votos
        with open(votes_file, 'w') as f:
            json.dump(votes, f, ensure_ascii=False, indent=2)
    
    def get_today_votes(self) -> List[Dict]:
        """Obtiene los votos del día"""
        today = self._get_today_date()
        votes_file = f"data/votes_{today}.json"
        
        if os.path.exists(votes_file):
            with open(votes_file, 'r') as f:
                return json.load(f)
        return []

# Instancia global
daily_affirmation = DailyAffirmation() 