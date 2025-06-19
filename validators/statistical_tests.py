import math
from typing import List, Dict, Any
from scipy import stats
import numpy as np

class ChiSquareTest:
    """Prueba de bondad de ajuste Chi-cuadrado"""
    
    def __init__(self):
        # Tabla de valores críticos para Chi-cuadrado
        # Filas: grados de libertad (1-30), Columnas: niveles de significancia
        self.critical_values_table = {
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
    
    def get_critical_value(self, degrees_of_freedom: int, alpha: float) -> float:
        """Obtener valor crítico de Chi-cuadrado para los grados de libertad y nivel de significancia dados"""
        
        # Verificar si tenemos el valor en la tabla
        if alpha in self.critical_values_table:
            if degrees_of_freedom in self.critical_values_table[alpha]:
                return self.critical_values_table[alpha][degrees_of_freedom]
        
        # Si no está en la tabla, usar scipy para calcularlo
        try:
            # Usar el percentil (1 - alpha) de la distribución chi-cuadrado
            return stats.chi2.ppf(1 - alpha, degrees_of_freedom)
        except Exception:
            # Fallback: usar valor por defecto para α = 0.05
            return stats.chi2.ppf(0.95, degrees_of_freedom)
    
    def run_test(self, numbers: List[float], intervals: int, alpha: float = 0.05) -> Dict[str, Any]:
        """Ejecutar prueba Chi-cuadrado"""
        try:
            # Validar parámetros
            if not numbers:
                raise ValueError("La lista de números no puede estar vacía")
            
            if intervals < 2:
                raise ValueError("El número de intervalos debe ser mayor o igual a 2")
            
            if alpha not in [0.01, 0.05, 0.10]:
                raise ValueError("El nivel de significancia debe ser 0.01, 0.05 o 0.10")
            
            # Normalizar números al rango [0, 1] si es necesario
            min_val = min(numbers)
            max_val = max(numbers)
            
            if min_val == max_val:
                raise ValueError("Todos los números son iguales, no se puede realizar la prueba")
            
            # Normalizar solo si los números no están en el rango [0,1]
            if min_val < 0 or max_val > 1:
                normalized = [(x - min_val) / (max_val - min_val) for x in numbers]
            else:
                normalized = numbers.copy()
            
            # Crear intervalos
            interval_width = 1.0 / intervals
            observed_frequencies = [0] * intervals
            
            # Contar frecuencias observadas
            for num in normalized:
                # Asegurar que el número esté en [0,1]
                num = max(0, min(1, num))
                interval_index = min(int(num / interval_width), intervals - 1)
                observed_frequencies[interval_index] += 1
            
            # Frecuencia esperada (distribución uniforme)
            n = len(numbers)
            expected_frequency = n / intervals
            
            # Verificar que la frecuencia esperada sea suficiente (regla general: FE >= 5)
            if expected_frequency < 5:
                import warnings
                warnings.warn(f"Frecuencia esperada ({expected_frequency:.2f}) es menor a 5. "
                            "Los resultados pueden no ser confiables.")
            
            # Calcular estadístico Chi-cuadrado
            chi_square = 0
            for observed in observed_frequencies:
                chi_square += (observed - expected_frequency) ** 2 / expected_frequency
            
            # Grados de libertad
            degrees_of_freedom = intervals - 1
            
            # Valor crítico basado en α seleccionado
            critical_value = self.get_critical_value(degrees_of_freedom, alpha)
            
            # Resultado de la prueba
            passes = chi_square <= critical_value
            
            # Calcular p-valor usando scipy
            try:
                p_value = 1 - stats.chi2.cdf(chi_square, degrees_of_freedom)
            except Exception:
                p_value = None
            
            # Crear detalles de la prueba
            details = f"N = {n}, K = {intervals}, "
            details += f"Frecuencias observadas: {observed_frequencies}, "
            details += f"Frecuencia esperada: {expected_frequency:.2f}, "
            details += f"Grados de libertad: {degrees_of_freedom}, "
            details += f"α = {alpha}"
            
            # Determinar nivel de confianza
            confidence_level = int((1 - alpha) * 100)
            
            result = {
                "test_name": "Chi-cuadrado",
                "calculated_value": round(chi_square, 6),
                "critical_value": round(critical_value, 6),
                "passes": passes,
                "details": details,
                "alpha": alpha,
                "confidence_level": f"{confidence_level}%",
                "degrees_of_freedom": degrees_of_freedom,
                "sample_size": n,
                "intervals": intervals,
                "observed_frequencies": observed_frequencies,
                "expected_frequency": round(expected_frequency, 2)
            }
            
            if p_value is not None:
                result["p_value"] = round(p_value, 6)
            
            return result
            
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
            if not numbers:
                raise ValueError("La lista de números no puede estar vacía")
            
            # Normalizar números al rango [0, 1]
            min_val = min(numbers)
            max_val = max(numbers)
            
            if min_val == max_val:
                raise ValueError("Todos los números son iguales, no se puede realizar la prueba")
            
            # Normalizar solo si los números no están en el rango [0,1]
            if min_val < 0 or max_val > 1:
                normalized = [(x - min_val) / (max_val - min_val) for x in numbers]
            else:
                normalized = numbers.copy()
            
            normalized.sort()
            n = len(normalized)
            
            # Calcular diferencias máximas según el método del PDF
            max_diff = 0
            
            for i, y_i in enumerate(normalized):
                # i+1 porque el índice en el PDF empieza en 1
                theoretical_cdf = (i + 1) / n  # i/n en el PDF
                empirical_cdf = y_i
                
                # Calcular |y(i) - i/n| como indica el PDF
                diff = abs(empirical_cdf - theoretical_cdf)
                max_diff = max(max_diff, diff)
            
            # Valor crítico
            coefficient = self.critical_coefficients.get(significance_level, 1.36)
            critical_value = coefficient / math.sqrt(n)
            
            # Resultado
            passes = max_diff <= critical_value
            
            # Calcular p-valor aproximado usando scipy
            try:
                ks_statistic, p_value = stats.kstest(normalized, 'uniform')
                p_value = p_value if not math.isnan(p_value) else None
            except:
                p_value = None
            
            confidence_level = int((1 - significance_level) * 100)
            
            details = f"n = {n}, α = {significance_level}, "
            details += f"Coeficiente crítico = {coefficient}"
            
            result = {
                "test_name": "Kolmogorov-Smirnov",
                "calculated_value": round(max_diff, 6),
                "critical_value": round(critical_value, 6),
                "passes": passes,
                "details": details,
                "alpha": significance_level,
                "confidence_level": f"{confidence_level}%",
                "sample_size": n
            }
            
            if p_value is not None:
                result["p_value"] = round(p_value, 6)
            
            return result
            
        except Exception as e:
            raise ValueError(f"Error en prueba Kolmogorov-Smirnov: {str(e)}")