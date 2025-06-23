from abc import ABC, abstractmethod
import random
import math
from typing import List, Dict, Any, Tuple

class AcceptanceRejectionGenerator(ABC):
    """Generador de variables aleatorias usando método de aceptación-rechazo"""
    
    def __init__(self, a, b, M, function_name: str):
        random.seed()  # Usar semilla basada en tiempo
        self.a = a
        self.b = b
        self.M = M
        self.function_name = function_name

    @abstractmethod
    def target_density(self, x: float) -> float:
        """Función de densidad objetivo f(x)"""
        pass

    def get_function_name(self) -> str:
        """Obtener el nombre de la función de densidad objetivo f(x)"""
        return self.function_name
    
    def generate_function_points(self):
        """Generar puntos para la función de densidad f(x)"""
        points_x = []
        points_y = []
        for i in range(100):
            x = i / 100 *(self.b - self.a) + self.a  # Escalar x entre a y b
            y = self.target_density(x)
            points_x.append(x)
            points_y.append(y)
        return points_x, points_y

    def generate(self, count: int) -> Dict[str, Any]:
        """
        Generar variables aleatorias con densidad f(x) usando aceptación-rechazo
        
        Args:
            count: Número de valores a generar
            
        Returns:
            Diccionario con los resultados
        """
        # La constante M debe satisfacer f(x) <= M * g(x) para todo x
        # Para f(x) = 2x y g(x) = 1, tenemos M = 2 (máximo de f(x) en [0,1])
        
        
        r1_values = []  # Números aleatorios para x
        r2_values = []  # Números aleatorios para y
        accepted_values = []
        chart_x = []
        chart_y = []
        chart_accepted = []
        
        chart_x_d = []
        chart_y_d = []
        points_x_d, points_fx_d = self.generate_function_points()
        accepted_count = 0
        
        
        # Generar hasta obtener 'count' valores aceptados
        for i in range(count):
            # Generar x de la distribución auxiliar
            r1 = random.random() 
            r1_values.append(r1)

            r2 = random.random()
            r2_values.append(r2)
            
            vax = (self.a) + (self.b - self.a) * r1  
            

            fvax = self.target_density(vax)
            
            
            chart_x_d.append(vax)
            chart_y_d.append(r2 * self.M)
            
            # Datos para el gráfico
            chart_x.append(i + 1)
            chart_y.append(fvax / self.M)

            # Criterio de aceptación: r2 <= f(x)/M
            if r2 <= fvax / self.M:
                accepted_values.append(vax)
                chart_accepted.append(True)
                accepted_count += 1
            else:
                chart_accepted.append(False)
            
        
        
        # Calcular tasa de aceptación
        acceptance_rate = accepted_count / count if count > 0 else 0
        
        return {
            "r1": r1_values,
            "r2": r2_values,
            "generated_values": accepted_values,
            "acceptance_rate": acceptance_rate,
            "chart_data": {
                "function_name": self.get_function_name(),
                "x": chart_x,
                "y": chart_y,
                "r2": r2_values,
                "accepted": chart_accepted,
                "x_d": chart_x_d,
                "y_d": chart_y_d,
                "points_fx_d": points_fx_d,
                "points_x_d": points_x_d,
                "a": self.a,
                "b": self.b,
                "M": self.M
            }
        }

class LinealFunction(AcceptanceRejectionGenerator):

    def __init__(self):
        # Definir los parámetros de la función lineal
        a = 0
        b = 1
        M = 2
        function_name = "f(x) = 2x"
        super().__init__(a, b, M, function_name=function_name)

    def target_density(self, x: float) -> float:
        """Función de densidad objetivo f(x) = 2x para x en [0, 1]"""
        if self.a <= x <= self.b:
            return 2 * x
        return 0


class CuadraticFunction(AcceptanceRejectionGenerator):

    def __init__(self):
        # Definir los parámetros de la función cuadrática
        a = 0
        b = 4
        M = 4
        function_name = "f(x) = -(x-2)^2 + 4"
        super().__init__(a, b, M, function_name=function_name)

    def target_density(self, x: float) -> float:
        """Función de densidad objetivo f(x) = -(x-2)**(2) + 4 para x en [0, 4]"""
        if self.a <= x <= self.b:
            return -(x-2)**(2) + 4
        return 0

class HyperbolaFunction(AcceptanceRejectionGenerator):

    def __init__(self):
        # Definir los parámetros de la función hiperbólica
        a = 0.5
        b = 3
        M = 2
        function_name = "f(x) = 1/x"
        super().__init__(a, b, M, function_name=function_name)

    def target_density(self, x: float) -> float:
        """Función de densidad objetivo f(x) = 1/x para x en [0.5, 3]"""
        if self.a <= x <= self.b:
            return 1 / x
        return 0