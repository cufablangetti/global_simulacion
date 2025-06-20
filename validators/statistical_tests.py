import math
from typing import List, Dict, Any
from scipy import stats
import numpy as np

class ChiSquareTest:
    """Prueba de bondad de ajuste Chi-cuadrado"""
    
    def __init__(self):
        self.critical_values = {
            # Grados de libertad
            # α = 0.01 (99% confianza)
            0.01: {
                1: 6.635, 2: 9.210, 3: 11.345, 4: 13.277, 5: 15.086,
                6: 16.812, 7: 18.475, 8: 20.090, 9: 21.666, 10: 23.209,
                11: 24.725, 12: 26.217, 13: 27.688, 14: 29.141, 15: 30.578,
                16: 32.000, 17: 33.409, 18: 34.805, 19: 36.191, 20: 37.566,
                21: 38.932, 22: 40.289, 23: 41.638, 24: 42.980, 25: 44.314,
                26: 45.642, 27: 46.963, 28: 48.278, 29: 49.588, 30: 50.892
            },
            # α = 0.05 (95% confianza)
            0.05: {
                1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070,
                6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919, 10: 18.307,
                11: 19.675, 12: 21.026, 13: 22.362, 14: 23.685, 15: 24.996,
                16: 26.296, 17: 27.587, 18: 28.869, 19: 30.144, 20: 31.410,
                21: 32.671, 22: 33.924, 23: 35.172, 24: 36.415, 25: 37.652,
                26: 38.885, 27: 40.113, 28: 41.337, 29: 42.557, 30: 43.773
            },
            # α = 0.10 (90% confianza)
            0.10: {
                1: 2.706, 2: 4.605, 3: 6.251, 4: 7.779, 5: 9.236,
                6: 10.645, 7: 12.017, 8: 13.362, 9: 14.684, 10: 15.987,
                11: 17.275, 12: 18.549, 13: 19.812, 14: 21.064, 15: 22.307,
                16: 23.542, 17: 24.769, 18: 25.989, 19: 27.204, 20: 28.412,
                21: 29.615, 22: 30.813, 23: 32.007, 24: 33.196, 25: 34.382,
                26: 35.563, 27: 36.741, 28: 37.916, 29: 39.087, 30: 40.256
            }
        }
    
    def run_test(self, numbers: List[float], intervals: int, significance_level: float) -> Dict[str, Any]:
        """Ejecutar prueba Chi-cuadrado"""
        try:
            # Normalizar números al rango [0, 1] si es necesario
            min_val = min(numbers)
            max_val = max(numbers)
            
            if min_val == max_val:
                raise ValueError("Todos los números son iguales, no se puede realizar la prueba")
            
            normalized = [(x - min_val) / (max_val - min_val) for x in numbers]
            
            # Crear intervalos
            interval_width = 1.0 / intervals
            observed_frequencies = [0] * intervals
            
            # Contar frecuencias observadas
            for num in normalized:
                interval_index = min(int(num / interval_width), intervals - 1)
                observed_frequencies[interval_index] += 1
            
            # Frecuencia esperada (distribución uniforme)
            expected_frequency = len(numbers) / intervals
            
            # Calcular estadístico Chi-cuadrado
            chi_square = sum(
                (observed - expected_frequency) ** 2 / expected_frequency
                for observed in observed_frequencies
            )
            
            # Grados de libertad
            degrees_of_freedom = intervals - 1
            
            # Valor crítico
            criticals_for_alpha = self.critical_values.get(significance_level)
            if criticals_for_alpha and degrees_of_freedom in criticals_for_alpha:
                critical_value = criticals_for_alpha[degrees_of_freedom]
            else:
                # fallback: cálculo dinámico si no está en la tabla
                critical_value = stats.chi2.ppf(1 - significance_level, degrees_of_freedom)
            
            # Resultado
            passes = chi_square <= critical_value
            
            details = f"Frecuencias observadas: {observed_frequencies}, "
            details += f"Frecuencia esperada: {expected_frequency:.2f}, "
            details += f"Grados de libertad: {degrees_of_freedom}"
            
            return {
                "test_name": "Chi-cuadrado",
                "calculated_value": chi_square,
                "critical_value": critical_value,
                "passes": passes,
                "details": details
            }
            
        except Exception as e:
            raise ValueError(f"Error en prueba Chi-cuadrado: {str(e)}")

class KolmogorovSmirnovTest:
    """Prueba de bondad de ajuste Kolmogorov-Smirnov"""
    
    def __init__(self):
        # Valores críticos para diferentes niveles de significancia
        self.critical_coefficients = {
            0.01: [
                0.995, 0.929, 0.829, 0.734, 0.669, 0.617, 0.576, 0.542, 0.513, 0.489,
                0.468, 0.449, 0.432, 0.418, 0.404, 0.392, 0.381, 0.371, 0.361, 0.352,
                0.344, 0.337, 0.33, 0.323, 0.317, 0.311, 0.305, 0.300, 0.295, 0.290,
                0.285, 0.281, 0.277, 0.273, 0.269, 0.265, 0.262, 0.258, 0.255, 0.252
            ]
            ,
            0.05: [
                0.975, 0.842, 0.708, 0.624, 0.563, 0.519, 0.483, 0.454, 0.430, 0.409,
                0.391, 0.375, 0.361, 0.349, 0.338, 0.327, 0.318, 0.309, 0.301, 0.294,
                0.287, 0.281, 0.275, 0.269, 0.264, 0.259, 0.254, 0.250, 0.246, 0.242,
                0.238, 0.234, 0.231, 0.227, 0.224, 0.221, 0.218, 0.215, 0.213, 0.210
            ]
            ,
            0.10: [
                0.950, 0.776, 0.636, 0.656, 0.509, 0.468, 0.436, 0.410, 0.387, 0.369,
                0.352, 0.338, 0.325, 0.314, 0.304, 0.295, 0.286, 0.279, 0.271, 0.265,
                0.259, 0.253, 0.247, 0.242, 0.238, 0.233, 0.229, 0.225, 0.221, 0.218,
                0.214, 0.211, 0.208, 0.205, 0.202, 0.199, 0.196, 0.194, 0.191, 0.189
            ]
        }
    
    def run_test(self, y: List[float], significance_level: float = 0.05) -> Dict[str, Any]:
        """Ejecutar prueba Kolmogorov-Smirnov"""
        try:
            if not y:
                raise ValueError("La lista de datos está vacía")

            min_val = min(y)
            max_val = max(y)

            if min_val == max_val:
                raise ValueError("Todos los números son iguales, no se puede realizar la prueba")

            # Normalización al rango [0, 1]
            y = [(x - min_val) / (max_val - min_val) for x in y]
            y.sort()
            n = len(y)
            
            
            max_d = 0
            for i, x in enumerate(y):
                # Función de distribución empírica
                f = (i + 1) / n
                # Función de distribución teórica (uniforme)
                max_d = max(max_d, abs(f - x))
                
            
            
            # Valor crítico
            critical_value = self.critical_coefficients.get(significance_level)[n - 1] if n - 1 < len(self.critical_coefficients[significance_level]) else None
            if critical_value is None:  
                critical_value = 1.36 / math.sqrt(n)  # Valor crítico aproximado para n grande
            # Resultado
            passes = max_d <= critical_value
            
            # Calcular p-valor aproximado usando la distribución de Kolmogorov
            
            details = f"n = {n}, α = {significance_level}"
            
            result = {
                "test_name": "Kolmogorov-Smirnov",
                "calculated_value": max_d,
                "critical_value": critical_value,
                "passes": passes,
                "details": details
            }
            
            return result
            
        except Exception as e:
            raise ValueError(f"Error en prueba Kolmogorov-Smirnov: {str(e)}")