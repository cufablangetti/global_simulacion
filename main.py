from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn

from generators.congruential import MixedCongruentialGenerator, MultiplicativeCongruentialGenerator
from generators.middle_squares import MiddleSquaresGenerator
from validators.conditions import CongruentialValidator
from validators.statistical_tests import ChiSquareTest, KolmogorovSmirnovTest
from random_variables.acceptance_rejection import AcceptanceRejectionGenerator

app = FastAPI(title="Pseudorandom Number Generator API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class GenerationRequest(BaseModel):
    method: str
    parameters: Dict[str, float]

class ValidationRequest(BaseModel):
    method: str
    parameters: Dict[str, float]

class StatisticalTestRequest(BaseModel):
    numbers: List[float]
    test_type: str
    parameters: Dict[str, Any]

class RandomVariableRequest(BaseModel):
    count: int
    method: str
    distribution: str

@app.get("/health")
async def health_check():
    """Verificar estado del servidor"""
    return {"status": "ok", "message": "Backend funcionando correctamente"}

@app.post("/generate")
async def generate_numbers(request: GenerationRequest):
    """Generar números pseudoaleatorios"""
    try:
        method = request.method
        params = request.parameters
        
        if method == "mixed_congruential":
            generator = MixedCongruentialGenerator(
                x0=int(params["x0"]),
                a=int(params["a"]),
                b=int(params["b"]),
                m=int(params["m"])
            )
        elif method == "multiplicative_congruential":
            generator = MultiplicativeCongruentialGenerator(
                x0=int(params["x0"]),
                a=int(params["a"]),
                m=int(params["m"])
            )
        elif method == "middle_squares":
            generator = MiddleSquaresGenerator(
                x0=int(params["x0"]),
                digits=int(params["digits"])
            )
        else:
            raise HTTPException(status_code=400, detail="Método no válido")
        
        numbers, stats = generator.generate()
        
        return {
            "numbers": numbers,
            "statistics": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate")
async def validate_conditions(request: ValidationRequest):
    """Validar condiciones teóricas de los métodos congruenciales"""
    try:
        if not request.method.endswith("congruential"):
            raise HTTPException(status_code=400, detail="Validación solo disponible para métodos congruenciales")
        
        params = request.parameters
        validator = CongruentialValidator(
            a=int(params["a"]),
            b=int(params.get("b", 0)),
            m=int(params["m"]),
            is_mixed=request.method == "mixed_congruential"
        )
        
        conditions = validator.validate_all_conditions()
        
        return {
            "conditions": conditions,
            "all_satisfied": all(c["satisfied"] for c in conditions),
            "explanation": validator.get_explanation()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/statistical-test")
async def run_statistical_test(request: StatisticalTestRequest):
    """Ejecutar pruebas estadísticas"""
    try:
        numbers = request.numbers
        test_type = request.test_type
        params = request.parameters
        
        if test_type == "chi_square":
            test = ChiSquareTest()
            result = test.run_test(numbers, params["intervals"])
        elif test_type == "kolmogorov_smirnov":
            test = KolmogorovSmirnovTest()
            result = test.run_test(numbers, params["significance_level"])
        else:
            raise HTTPException(status_code=400, detail="Tipo de prueba no válido")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/random-variables")
async def generate_random_variables(request: RandomVariableRequest):
    """Generar variables aleatorias usando método de aceptación-rechazo"""
    try:
        if request.method != "acceptance_rejection":
            raise HTTPException(status_code=400, detail="Método no válido")
        
        generator = AcceptanceRejectionGenerator()
        result = generator.generate_triangular(request.count)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)