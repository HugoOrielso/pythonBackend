from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from fractions import Fraction


app = Flask(__name__)
CORS(app)  

@app.route("/", methods=["GET"])
def sls():
    return "Hola"

@app.route('/sumar', methods=['POST'])
def suma():
    try:
        
        if not request.json or ("matrizUno" not in request.json or "matrizDos" not in request.json):
            return jsonify({"error": "Faltan datos por enviar (matrizUno o matrizDos).", "status": "error"}), 400

        matriz_a = np.array(request.json["matrizUno"])
        matriz_b = np.array(request.json["matrizDos"])

        if matriz_a.shape != matriz_b.shape:
            return jsonify({"error": "Las dimensiones de las matrices no coinciden."}), 400

        resultado = np.add(matriz_a, matriz_b)
        return jsonify({"resultado": resultado.tolist(),
                        "status": "success"})

    except ValueError:
        return jsonify({"error": "Formato de matriz inválido."}), 400
    
@app.route('/restar', methods=['POST'])
def restar():
    try:
        
        if not request.json or ("matrizUno" not in request.json or "matrizDos" not in request.json):
            return jsonify({"error": "Faltan datos por enviar (matrizUno o matrizDos).", "status": "error"}), 400

        matriz_a = np.array(request.json["matrizUno"])
        matriz_b = np.array(request.json["matrizDos"])
            

        if matriz_a.shape != matriz_b.shape:
            return jsonify({"error": "Las dimensiones de las matrices no coinciden."}), 400

        resultado = np.subtract(matriz_a, matriz_b)
        return jsonify({"resultado": resultado.tolist(),
                        "status": "success"})

    except ValueError:
        return jsonify({"error": "Formato de matriz inválido."}), 400


@app.route('/multiplicar', methods=['POST'])
def multiplicar():
    try:
        if not request.json or ("matrizUno" not in request.json or "matrizDos" not in request.json):
            return jsonify({"error": "Faltan datos por enviar (matrizUno o matrizDos).", "status": "error"}), 400

        matriz_a = np.array(request.json["matrizUno"])
        matriz_b = np.array(request.json["matrizDos"])

        # Verificar si las matrices se pueden multiplicar
        if matriz_a.shape[1] != matriz_b.shape[0]:
            return jsonify({"error": "Las dimensiones de las matrices no son compatibles para multiplicación.", "status": "error"}), 400

        resultado = np.matmul(matriz_a, matriz_b)
        return jsonify({"resultado": resultado.tolist(),
                        "status": "success"})

    except ValueError:
        return jsonify({"error": "Formato de matriz inválido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/transpuesta', methods=['POST'])
def transpuesta():
    try:
        if not request.json or ("matrizUno" not in request.json):
            return jsonify({"error": "Faltan datos por enviar.", "status": "error"}), 400

        matriz_a = np.array(request.json["matrizUno"])

        resultado = matriz_a.T
        return jsonify({"resultado": resultado.tolist(),
                        "status": "success"})
    
    except ValueError:
        return jsonify({"error"})

    except Exception as e:
        return jsonify({"error": str(e),"status": "error"}), 500
    
    
@app.route('/inversa', methods=['POST'])
def inversa():
    try:
        if not request.json or ("matrizUno" not in request.json):
            return jsonify({"error": "Faltan datos por enviar.", "status": "error"}), 400

        matriz_a =(request.json["matrizUno"])

        if not isinstance(matriz_a, list) or not all(isinstance(row, list) for row in matriz_a):
            return jsonify({"error": "La matriz debe ser una lista de listas.", "status": "error"}), 400

        matriz_a = np.array(matriz_a)

        if matriz_a.shape[0] != matriz_a.shape[1]:
            return jsonify({"error": "La matriz debe ser cuadrada.", "status": "error"}), 400

        try:
            resultado = np.linalg.inv(matriz_a)
        except np.linalg.LinAlgError:
            return jsonify({"error": "La matriz no es invertible.", "status": "error"}), 400

        response_data = {"resultado": resultado.tolist(), "status": "success"}
        return jsonify((response_data))

    except ValueError as e:
        return jsonify({"error": f"Error de valor: {str(e)}", "status": "error"}), 400

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}", "status": "error"}), 500
    
def es_cuadrada(matriz):
    return all(len(fila) == len(matriz) for fila in matriz)

def es_diagonal(matriz):
    if not es_cuadrada(matriz):
        return False
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if i != j and matriz[i][j] != 0:
                return False
    return True

def es_identidad(matriz):
    if not es_diagonal(matriz):
        return False
    for i in range(len(matriz)):
        if matriz[i][i] != 1:
            return False
    return True

def es_nula(matriz):
    for fila in matriz:
        for elemento in fila:
            if elemento != 0:
                return False
    return True

def es_simetrica(matriz):
    if not es_cuadrada(matriz):
        return False
    matriz_np = np.array(matriz)
    return np.array_equal(matriz_np, matriz_np.T)

def es_triangular_superior(matriz):
    if not es_cuadrada(matriz):
        return False
    for i in range(1, len(matriz)):
        for j in range(i):
            if matriz[i][j] != 0:
                return False
    return True

def es_triangular_inferior(matriz):
    if not es_cuadrada(matriz):
        return False
    for i in range(len(matriz) - 1):
        for j in range(i + 1, len(matriz)):
            if matriz[i][j] != 0:
                return False
    return True

def es_ortogonal(matriz):
    if not es_cuadrada(matriz):
        return False
    matriz_np = np.array(matriz)
    identidad = np.eye(len(matriz))
    return np.allclose(matriz_np @ matriz_np.T, identidad)

def es_escalar(matriz):
    if not es_diagonal(matriz):
        return False
    valor = matriz[0][0]
    for i in range(1, len(matriz)):
        if matriz[i][i] != valor:
            return False
    return True



@app.route('/tipo', methods=['POST'])
def tipo_matriz():
    try:
        if not request.json or ("matrizUno" not in request.json):
            return jsonify({"error": "Faltan datos por enviar.", "status": "error"}), 400

        matriz = np.array(request.json["matrizUno"])
        
        print(matriz)

        resultados = {
            "es_cuadrada": bool(es_cuadrada(matriz)),
            "es_diagonal": bool(es_diagonal(matriz)),
            "es_identidad": bool(es_identidad(matriz)),
            "es_nula": bool(es_nula(matriz)),
            "es_simetrica": bool(es_simetrica(matriz)),
            "es_triangular_superior": bool(es_triangular_superior(matriz)),
            "es_triangular_inferior": bool(es_triangular_inferior(matriz)),
            "es_ortogonal": bool(es_ortogonal(matriz)),
            "es_escalar": bool(es_escalar(matriz))
        }

        tipo = []
        if resultados["es_cuadrada"]:
            tipo.append("cuadrada")
        if resultados["es_diagonal"]:
            tipo.append("diagonal")
        if resultados["es_identidad"]:
            tipo.append("identidad")
        if resultados["es_nula"]:
            tipo.append("nula")
        if resultados["es_simetrica"]:
            tipo.append("simétrica")
        if resultados["es_triangular_superior"]:
            tipo.append("triangular superior")
        if resultados["es_triangular_inferior"]:
            tipo.append("triangular inferior")
        if resultados["es_ortogonal"]:
            tipo.append("ortogonal")
        if resultados["es_escalar"]:
            tipo.append("escalar")

        if not tipo:
            tipo.append("ninguno de los tipos reconocidos")

        return jsonify({
            "tipo": tipo,
            "detalles": resultados,
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({"error": f"Se produjo un error: {str(e)}"}), 500




if __name__ == '__main__':
    app.run(debug=True, port=4321)