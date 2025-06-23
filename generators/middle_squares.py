from typing import List, Tuple, Dict, Any

class MiddleSquaresGenerator:
    # Generador de cuadrados medios
    
    def __init__(self, x0: int, digits: int):
        self.x0 = x0
        self.digits = digits
        self.sequence = []
        self.seen_values = set()
        self.base = 10 ** self.digits
    
    def extract_middle_digits(self, squared: int) -> int:
        # Extraer los dígitos medios de un número
        squared_str = str(squared).ljust(2 * self.digits, "0") # Asegurar que tenga suficientes dígitos, se agregan 0s a la derecha
        
        start = (len(squared_str) - self.digits) // 2 # Calcular el inicio de los dígitos medios, // es division entera
        middle = squared_str[start:start + self.digits] # Extraer los dígitos medios, [start:start + self.digits] es un slice
        return int(middle) # Convertir a entero
    
    def generate(self) -> Tuple[List[int], Dict[str, Any]]:
        # Generar la secuencia completa
        self.sequence = []
        self.seen_values = set()
        
        current = self.x0
        max_iterations = 10000
        iterations = 0
        
        while current not in self.seen_values and iterations < max_iterations:
            self.seen_values.add(current)
            self.sequence.append(current)
            
            # Calcular siguiente valor
            squared = current ** 2
            current = self.extract_middle_digits(squared)
            
            # Detectar si empezamos a generar ceros
            # Si obtenemos un 0, detenemos inmediatamente
            if current == 0:
                stopped_reason = "Se generó un 0, lo cual hace que la secuencia se congele en ceros"
                break

            iterations += 1
        
        # Determinar razón de parada
        if iterations >= max_iterations:
            stopped_reason = f"Se alcanzó el límite máximo de iteraciones ({max_iterations})"
        elif current in self.seen_values:
            stopped_reason = f"Se repitió el valor {current}"
        
        normalized = [round(x / self.base, 3) for x in self.sequence]  # Números aleatorios en [0, 1)

        # Estadísticas
        stats = {
            "count": len(self.sequence),
            "min": min(self.sequence) if self.sequence else 0,
            "max": max(self.sequence) if self.sequence else 0,
            "mean": sum(self.sequence) / len(self.sequence) if self.sequence else 0,
            "stopped_reason": stopped_reason
        }
        
        return self.sequence, normalized, stats