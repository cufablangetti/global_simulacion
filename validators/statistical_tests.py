import math
from typing import List, Dict, Any
from scipy import stats
import numpy as np

class ChiSquareTest:
    """Prueba de bondad de ajuste Chi-cuadrado"""
    
    def __init__(self):
        self.critical_values = {
            # Grados de libertad: valor crítico (α = 0.05)
            1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070,
            6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919, 10: 18.307,
            11: 19.675, 12: 21.026, 13: 22.362, 14: 23.685, 15: 24.996,
            16: 26.296, 17: 27.587, 18: 28.869, 19: 30.144, 20: 31.410,
            25: 37.652, 30: 43.773
        }
    
    def run_test(self, numbers: List[float], intervals: int) -> Dict[str, Any]:
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
            critical_value = self.critical_values.get(degrees_of_freedom)
            if critical_value is None:
                # Usar distribución chi-cuadrado para grados de libertad no tabulados
                critical_value = stats.chi2.ppf(0.95, degrees_of_freedom)
            
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
            try:
                # Usar scipy para calcular p-valor más preciso
                ks_statistic, p_value = stats.kstest(normalized, 'uniform')
                p_value = p_value if not math.isnan(p_value) else None
            except:
                p_value = None
            
            details = f"D+ = {d_plus:.4f}, D- = {d_minus:.4f}, "
            details += f"n = {n}, α = {significance_level}"
            
            result = {
                "test_name": "Kolmogorov-Smirnov",
                "calculated_value": d_statistic,
                "critical_value": critical_value,
                "passes": passes,
                "details": details
            }
            
            if p_value is not None:
                result["p_value"] = p_value
            
            return result
            
        except Exception as e:
            raise ValueError(f"Error en prueba Kolmogorov-Smirnov: {str(e)}")