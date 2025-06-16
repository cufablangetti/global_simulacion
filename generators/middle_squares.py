import math
from typing import List, Tuple, Dict, Any

class MiddleSquaresGenerator:
    """Generador de cuadrados medios"""
    
    def __init__(self, x0: int, digits: int):
        self.x0 = x0
        self.digits = digits
        self.sequence = []
        self.seen_values = set()
    
    def extract_middle_digits(self, squared: int) -> int:
        """Extraer los dígitos medios de un número"""
        squared_str = str(squared).zfill(2 * self.digits)
        start = (len(squared_str) - self.digits) // 2
        middle = squared_str[start:start + self.digits]
        return int(middle)
    
    def generate(self) -> Tuple[List[int], Dict[str, Any]]:
        """Generar la secuencia completa"""
        self.sequence = []
        self.seen_values = set()
        
        current = self.x0
        zero_count = 0
        max_iterations = 10000
        iterations = 0
        
        while current not in self.seen_values and iterations < max_iterations:
            self.seen_values.add(current)
            self.sequence.append(current)
            
            # Calcular siguiente valor
            squared = current * current
            current = self.extract_middle_digits(squared)
            
            # Detectar si empezamos a generar ceros
            if current == 0:
                zero_count += 1
                if zero_count >= 3:  # Si generamos 3 ceros seguidos, parar
                    self.sequence.append(current)
                    break
            else:
                zero_count = 0
            
            iterations += 1
        
        # Determinar razón de parada
        if iterations >= max_iterations:
            stopped_reason = f"Se alcanzó el límite máximo de iteraciones ({max_iterations})"
        elif current in self.seen_values:
            stopped_reason = f"Se repitió el valor {current}"
        elif zero_count >= 3:
            stopped_reason = "Se generaron múltiples ceros consecutivos"
        else:
            stopped_reason = "Generación completada"
        
        # Estadísticas
        stats = {
            "count": len(self.sequence),
            "min": min(self.sequence) if self.sequence else 0,
            "max": max(self.sequence) if self.sequence else 0,
            "mean": sum(self.sequence) / len(self.sequence) if self.sequence else 0,
            "stopped_reason": stopped_reason
        }
        
        return self.sequence, stats