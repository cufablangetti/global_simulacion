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
            0.01: 1.628,
            0.05: 1.36,
            0.10: 1.22
        }
    
    def run_test(self, numbers: List[float], significance_level: float = 0.05) -> Dict[str, Any]:
        """Ejecutar prueba Kolmogorov-Smirnov"""
        try:
            # Normalizar números al rango [0, 1]
            min_val = min(numbers)
            max_val = max(numbers)
            
            if min_val == max_val:
                raise ValueError("Todos los números son iguales, no se puede realizar la prueba")
            
            normalized = [(x - min_val) / (max_val - min_val) for x in numbers]
            normalized.sort()
            
            n = len(normalized)
            
            # Calcular D+ y D-
            d_plus = 0
            d_minus = 0
            
            for i, x in enumerate(normalized):
                # Función de distribución empírica
                f_empirical = (i + 1) / n
                # Función de distribución teórica (uniforme)
                f_theoretical = x
                
                d_plus = max(d_plus, f_empirical - f_theoretical)
                d_minus = max(d_minus, f_theoretical - f_empirical)
            
            # Estadístico D
            d_statistic = max(d_plus, d_minus)
            
            # Valor crítico
            coefficient = self.critical_coefficients.get(significance_level, 1.36)
            critical_value = coefficient / math.sqrt(n)
            
            # Resultado
            passes = d_statistic <= critical_value
            
            # Calcular p-valor aproximado usando la distribución de Kolmogorov
            
            details = f"n = {n}, α = {significance_level}"
            
            result = {
                "test_name": "Kolmogorov-Smirnov",
                "calculated_value": d_statistic,
                "critical_value": critical_value,
                "passes": passes,
                "details": details
            }
            
            return result
            
        except Exception as e:
            raise ValueError(f"Error en prueba Kolmogorov-Smirnov: {str(e)}")