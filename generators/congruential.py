from typing import List, Tuple, Dict, Any
from abc import ABC, abstractmethod

class CongruentialGenerator(ABC):
    # Clase base para generadores congruenciales
    
    def __init__(self, x0: int, a: int, m: int):
        self.x0 = x0
        self.a = a
        self.m = m
        self.sequence = []
        self.seen_values = set()
    
    @abstractmethod
    def next_value(self, x: int) -> int:
        # Calcular el siguiente valor de la secuencia
        pass
    
    def generate(self) -> Tuple[List[int], Dict[str, Any]]:
        # Generar la secuencia completa hasta encontrar repetición
        self.sequence = []
        self.seen_values = set()
        
        current = self.x0
        
        while current not in self.seen_values:
            self.seen_values.add(current)
            self.sequence.append(current)
            current = self.next_value(current)
        
        normalized = [round(x / self.m, 3) for x in self.sequence]  # Números aleatorios en [0, 1)

        # Estadísticas
        stats = {
            "count": len(self.sequence),
            "min": min(self.sequence),
            "max": max(self.sequence),
            "mean": sum(self.sequence) / len(self.sequence),
            "period": len(self.sequence),
            "stopped_reason": f"Se repitió el valor {current} (inicio de ciclo)"
        }
        
        return self.sequence, normalized, stats

class MixedCongruentialGenerator(CongruentialGenerator):
    # Generador congruencial mixto: X(n+1) = (a*X(n) + b) mod m
    
    def __init__(self, x0: int, a: int, b: int, m: int):
        super().__init__(x0, a, m)
        self.b = b
    
    def next_value(self, x: int) -> int:
        return (self.a * x + self.b) % self.m

class MultiplicativeCongruentialGenerator(CongruentialGenerator):
    # Generador congruencial multiplicativo: X(n+1) = (a*X(n)) mod m
    
    def next_value(self, x: int) -> int:
        return (self.a * x) % self.m