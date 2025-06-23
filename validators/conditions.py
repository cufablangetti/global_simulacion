import math
from typing import List, Dict, Any

class CongruentialValidator:
    """Validador de condiciones teóricas para generadores congruenciales"""
    
    def __init__(self, a: int, b: int, m: int, is_mixed: bool = True):
        self.a = a
        self.b = b
        self.m = m
        self.is_mixed = is_mixed
    
    def gcd(self, a: int, b: int) -> int:
        """Calcular máximo común divisor"""
        while b:
            a, b = b, a % b
        return a
    
    def get_prime_factors(self, n: int) -> List[int]:
        """Obtener factores primos de un número"""
        factors = []
        d = 2
        while d * d <= n:
            while (n % d) == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return list(set(factors))  # Eliminar duplicados
    
    def validate_gcd_condition(self) -> Dict[str, Any]:
        """Validar que gcd(b, m) = 1 para congruencial mixto"""
        if not self.is_mixed:
            return {
                "name": "mcd(b, m) = 1",
                "description": "No aplica para método multiplicativo",
                "satisfied": True,
                "details": "Esta condición solo se evalúa en el método mixto"
            }
        
        gcd_value = self.gcd(self.b, self.m)
        satisfied = gcd_value == 1
        
        return {
            "name": "mcd(b, m) = 1",
            "description": "b y m deben ser primos entre sí",
            "satisfied": satisfied,
            "details": f"mcd({self.b}, {self.m}) = {gcd_value}"
        }
    
    def validate_prime_divisor_condition(self) -> Dict[str, Any]:
        """Si q es un divisor primo de m, entonces q divide a (a-1)"""
        prime_factors = self.get_prime_factors(self.m)
        satisfied = True
        failing_primes = []
        
        for q in prime_factors:
            if (self.a - 1) % q != 0:
                satisfied = False
                failing_primes.append(q)
        
        if satisfied:
            details = f"Todos los factores primos de m ({prime_factors}) dividen a (a-1) = {self.a - 1}"
        else:
            details = f"Los factores primos {failing_primes} de m no dividen a (a-1) = {self.a - 1}"
        
        return {
            "name": "Condición de divisores primos",
            "description": "Si q divide a m, entonces q debe dividir a (a-1)",
            "satisfied": satisfied,
            "details": details
        }
    
    def validate_four_divisor_condition(self) -> Dict[str, Any]:
        """Si 4 divide a m, entonces 4 debe dividir a (a-1)"""
        if self.m % 4 != 0:
            return {
                "name": "Condición del 4",
                "description": "Si 4 divide a m, entonces 4 debe dividir a (a-1)",
                "satisfied": True,
                "details": f"4 no divide a m = {self.m}, condición no aplicable"
            }
        
        satisfied = (self.a - 1) % 4 == 0
        
        return {
            "name": "Condición del 4",
            "description": "Si 4 divide a m, entonces 4 debe dividir a (a-1)",
            "satisfied": satisfied,
            "details": f"4 divide a m = {self.m}, y (a-1) = {self.a - 1} {'es' if satisfied else 'no es'} divisible por 4"
        }
    
    def validate_a_range_condition(self) -> Dict[str, Any]:
        """Validar que 1 < a < m"""
        satisfied = 1 < self.a < self.m
        
        return {
            "name": "Rango de a",
            "description": "a debe estar en el rango (1, m)",
            "satisfied": satisfied,
            "details": f"a = {self.a}, m = {self.m}, condición: 1 < {self.a} < {self.m}"
        }
    
    def validate_all_conditions(self) -> List[Dict[str, Any]]:
        """Validar todas las condiciones aplicables"""
        conditions = [
            #self.validate_a_range_condition(),
            self.validate_gcd_condition(),
            self.validate_prime_divisor_condition(),
            self.validate_four_divisor_condition()
        ]
        
        return conditions
    
    def get_explanation(self) -> str:
        """Obtener explicación del resultado de validación"""
        conditions = self.validate_all_conditions()
        satisfied_count = sum(1 for c in conditions if c["satisfied"])
        total_conditions = len([c for c in conditions if "No aplica" not in c["description"]])
        
        if satisfied_count == len(conditions):
            return "Todas las condiciones teóricas se cumplen. El generador debería producir la secuencia completa de período máximo."
        else:
            unsatisfied = [c["name"] for c in conditions if not c["satisfied"]]
            return f"Se incumplen las siguientes condiciones: {', '.join(unsatisfied)}. Esto puede resultar en un período menor al máximo posible."