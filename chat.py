
from transformers import BertForQuestionAnswering, BertTokenizerFast, RetriBertConfig
import torch
import requests
import json
import re
from flask import request
# Importar
modelo= 'leo123/BERT-Preguntas-Respuestas-Posgrados'
model_preentrenado = BertForQuestionAnswering.from_pretrained(modelo)
tokenizador = BertTokenizerFast.from_pretrained(modelo)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(f'Working on {device}')
model_preentrenado = model_preentrenado.to(device)
def get_prediction(contexto, pregunta):
  #se toqueniza las preguntas y el contexto
  entradas = tokenizador.encode_plus(pregunta, contexto, return_tensors='pt').to(device)
  print(entradas)
  salida = model_preentrenado(**entradas)
  print(salida)
  inicio_respuesta = torch.argmax(salida[0])  
  final_respuesta = torch.argmax(salida[1]) + 1 
  print(inicio_respuesta)
  print(final_respuesta)
  respuesta = tokenizador.convert_tokens_to_string(tokenizador.convert_ids_to_tokens(entradas['input_ids'][0][inicio_respuesta:final_respuesta]))
  print(respuesta)
  return respuesta
def normalize_text(s):
  """Removing articles and punctuation, and standardizing whitespace are all typical text processing steps."""
  import string, re
 
  def white_space_fix(text):
    return " ".join(text.split())
  def remove_punc(text):
    exclude = set(string.punctuation)
    return "".join(ch for ch in text if ch not in exclude)
  def lower(text):
    return text.lower()

  return white_space_fix(remove_punc(lower(s)))

def exact_match(prediction, truth):
    return bool(normalize_text(prediction) == normalize_text(truth))

def compute_f1(prediction, truth):
  pred_tokens = normalize_text(prediction).split()
  truth_tokens = normalize_text(truth).split()
  
  # if either the prediction or the truth is no-answer then f1 = 1 if they agree, 0 otherwise
  if len(pred_tokens) == 0 or len(truth_tokens) == 0:
    return int(pred_tokens == truth_tokens)
  
  common_tokens = set(pred_tokens) & set(truth_tokens)
  
  # if there are no common tokens then f1 = 0
  if len(common_tokens) == 0:
    return 0
  
  prec = len(common_tokens) / len(pred_tokens)
  rec = len(common_tokens) / len(truth_tokens)
  
  return round(2 * (prec * rec) / (prec + rec), 2)
  
def get_response(pregunta):
  pregunta=pregunta
  palabra=pregunta.lower()
  palabra= re.sub("\,|\?|\¿","",palabra)
  contex=palabra.split(' ')
  arreglo=[]
  for i, f in enumerate(contex):
    arreglo.append(f)
  url3 = 'https://raw.githubusercontent.com/Leo646/TrabajoTitulacion/main/Base_Conocimientos/Base_Conocimientos2'
  resp = requests.get(url3)
  datos = json.loads(resp.text)
  contexto='';
  b=0
  for  data in datos['data']:
    frase=''
    for clave in data['palabras_clave']:
      if clave in arreglo:
        b=b+1
        for parrafo in data['parrafo']:
          frase=parrafo['context']
    if b>=2:
      contexto=frase     
    b=0
  
  final=len(pregunta)-1
  if pregunta[0]=='¿' and pregunta[final]=='?':
    if len(contexto)==0:
      return("No he podido encontra información para tu pregunta")
    else:
      prediction = get_prediction(contexto,pregunta)
      return prediction
      #return prediction
  else:
    return("Por favor!! ingrese la consulta en forma de pregunta ")
  

