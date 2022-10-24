"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd

def load_and_preprocess():
  
  data_dir = 'clusters_report.txt'
  with open(data_dir, "r") as file:
    data_example = file.readlines()
    data_example = [line.replace("\n", "") for line in data_example]
  return data_example

import re
def load_headers():
  put_together_data = []
  row_data = load_and_preprocess()
  row_data = row_data[0:2]
  row_data = [re.sub('  +','  ',line) for line in row_data] # reemplazar mas de 3 espacios en blanco por solo 2 
  split_data = [re.split(r'\s{2,}',line) for line in row_data]
  #split_data = [line.replace(" ","_") for line in row_data]
  split_data[1].extend([' '] * (len(split_data[0])-len(split_data[1]))) # igualar longitud de 2 listas, el caracter a usar va dentro de []
  put_together_data = [' '.join(z) for z in zip(split_data[0],split_data[1])] # unir 2 elemento por elemento de 2 listas
  put_together_data = [line.rstrip() for line in put_together_data] # str.srtrip para eliminar espacios en blanco al final de una palabra o frase
  put_together_data.remove('')
  put_together_data = [line.lower().replace(' ','_') for line in put_together_data]
  
  return put_together_data

import re
def load_rows():

  one_line_data = []
  ready_data = []
  row_data = load_and_preprocess()
  row_data = row_data[4:]
  row_data.append(' ')
  row_data = [re.sub('                      +','*',line) for line in row_data]
  row_data[28] = row_data[28].replace('control','control.')
  single_line = row_data[0]
  for i in range(len(row_data)):
    if row_data[i].startswith('*'):
       single_line = single_line + row_data[i] + " "
    if row_data[i].find('.') != -1:
      one_line_data.append(single_line)
      single_line = row_data[i+2]

  for s in one_line_data:
    s = s.replace('%','                   ')
    ready_data.append(re.split(r'\s{15,}',s))
  
  numbers = [ arr[0] for arr in ready_data]
  texs = [ arr[1] for arr in ready_data]
  #print(len(texs))

  for i,s in enumerate(texs):
    s = s.replace('*','')
    texs[i] = " ".join(s.split())
    

  one_line_data = []

  for i, s in enumerate(numbers):
    s = s.replace(',','.')
    one_line_data.append(re.split(r'\s{2,}',s)[1:])
    one_line_data[i].append(texs[i])

  return one_line_data



def ingest_data():
  columns = load_headers()
  rows = load_rows()
  df = pd.DataFrame(rows,columns=columns)
  df.cantidad_de_palabras_clave = df.cantidad_de_palabras_clave.astype(int)
  df.porcentaje_de_palabras_clave = df.porcentaje_de_palabras_clave.astype(int)
  df.cluster = df.cluster.astype(float) 
  return df
