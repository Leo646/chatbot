import os
from tokenize import String
from flask import Flask, jsonify, render_template
from flask import request
#from chat import get_response
from cha1 import get_response
import random

app = Flask(__name__ )
@app.get("/")
def index():
    return render_template("index3.html")


@app.post("/predict")
def predict():
    entradaDespedida=["adios","chao","hasta luego","nos vemos","gracias hasta luego"]
    entradasaludo=['buenas',
    'hola','buenas tardes','buenos dias',
    'buenos dias','buenas noches']
    saludoChat=["Hola!! ¿En qué te puedo ayudar?", "Holaaa!! ¿Cómo te puedo ayudar?","Muy buenas!! ¿Cuál es tu consulta?","Saludos!! ¿Qué te gustaría saber?"]
    despedidaChat=['Adios, Cuidate!!',"Hasta Luego",'Chao, Cuidate!']
    while True:    
        text= request.get_json().get("message").lower()
        for entrada in entradasaludo:
            if entrada==text :
                message={"answer":random.choice(saludoChat)}
                return jsonify(message)
        for despedida in entradaDespedida:
            if despedida==text.lower() :
                message={"answer":random.choice(despedidaChat)}
                return jsonify(message)  
        
        respose=get_response(text)
        message={"answer":respose}
        return jsonify(message)

