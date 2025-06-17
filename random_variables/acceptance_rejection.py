import random
import math
from typing import List, Dict, Any, Tuple

class AcceptanceRejectionGenerator:
    """Generador de variables aleatorias usando método de aceptación-rechazo"""
    
    def __init__(self):
        random.seed()  # Usar semilla basada en tiempo
        self.a = 0
        self.b = 1

    def target_density(self, x: float) -> float:
        """Función de densidad objetivo f(x) = 2x para x en [0, 1]"""
        if 0 <= x <= 1:
            return 2 * x
        return 0
    
    def auxiliary_density(self, x: float) -> float:
        """Función de densidad auxiliar g(x) = 1 (uniforme en [0, 1])"""
        if 0 <= x <= 1:
            return 1
        return 0
    
    
    def generate_triangular(self, count: int) -> Dict[str, Any]:
        """
        Generar variables aleatorias con densidad f(x) = 2x usando aceptación-rechazo
        
        Args:
            count: Número de valores a generar
            
        Returns:
            Diccionario con los resultados
        """
        # La constante M debe satisfacer f(x) <= M * g(x) para todo x
        # Para f(x) = 2x y g(x) = 1, tenemos M = 2 (máximo de f(x) en [0,1])
        M = 2.0
        
        r1_values = []  # Números aleatorios para x
        r2_values = []  # Números aleatorios para y
        accepted_values = []
        chart_x = []
        chart_y = []
        chart_accepted = []
        
        accepted_count = 0
        
        
        # Generar hasta obtener 'count' valores aceptados
        for i in range(count):
            # Generar x de la distribución auxiliar
            r1 = random.random() 
            r1_values.append(r1)

            r2 = random.random()
            r2_values.append(r2)
            
            x = (self.a) + (self.b - self.a) * r1  
            

            fx = self.target_density(x)
            
            
            # Datos para el gráfico
            chart_x.append(i + 1)
            chart_y.append(fx / M)
            
            # Criterio de aceptación: r2 <= f(x)/M
            if r2 <= fx / M:
                accepted_values.append(x)
                chart_accepted.append(True)
                accepted_count += 1
            else:
                chart_accepted.append(False)
            
        
        
        # Calcular tasa de aceptación
        acceptance_rate = accepted_count / count if count > 0 else 0
        print({
            "r1": r1_values,
            "r2": r2_values,
            "generated_values": accepted_values,
            "acceptance_rate": acceptance_rate,
            "chart_data": {
                "x": chart_x,
                "y": chart_y,
                "r2": r2_values,
                "accepted": chart_accepted
            }
        })
        return {
            "r1": r1_values,
            "r2": r2_values,
            "generated_values": accepted_values,
            "acceptance_rate": acceptance_rate,
            "chart_data": {
                "x": chart_x,
                "y": chart_y,
                "r2": r2_values,
                "accepted": chart_accepted
            }
        }