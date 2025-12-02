from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
# 1. Маршрут для GET-запроса
@app.get("/")
def root():
    return {"status": "API is running!"}

@app.get("/hello")
def hello():
    return {"message": "Hello! This is GET endpoint."}

# 2. Маршрут для POST-запроса (просто демонстрация)
@app.post("/echo")
def echo(data: dict):
    return {"you_sent": data}

# 3. Маршрут, принимающий число и возвращающий *число × 2*
@app.get("/double/{number}")
def double_number(number: str):
    # Проверка, что введено число
    if not number.replace(".", "", 1).isdigit():
        return {"error": "expected number, got string."}
    return {"result": float(number) * 2}

# 4. POST-маршрут → salary + bonus - taxes  (валидация полей)
class SalaryRequest(BaseModel):
    salary: float
    bonus: float
    taxes: float

@app.post("/calc")
def calculate(data: dict):
    required_fields = {"salary", "bonus", "taxes"}

    # Проверка количества полей
    missing = required_fields - data.keys()
    if missing:
        return {
            "error": f"3 fields expected (salary, bonus, taxes). You forgot: {', '.join(missing)}."
        }

    # Проверка, что все числа
    try:
        salary = float(data["salary"])
        bonus = float(data["bonus"])
        taxes = float(data["taxes"])
    except ValueError:
        return {"error": "expected numbers, got strings."}

    result = salary + bonus - taxes
    return {"result": result}