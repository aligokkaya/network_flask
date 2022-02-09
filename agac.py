from email import message
from dns.rdatatype import NULL
import numpy as np
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from flask import Flask, flash, request, redirect, url_for, current_app,send_from_directory,render_template, session
from scipy.ndimage import measurements
from wtforms import Form,StringField,TextAreaField,form,validators
from werkzeug.utils import secure_filename
from datetime import  datetime
from functools import wraps
import base64
import re
import pandas as pd
import random
import wtforms
from wtforms.fields.html5 import TelField,IntegerField
from wtforms.fields.core import DateField, DateTimeField, FormField

from datetime import datetime
from datetime import timedelta
import easyocr
import cv2
import networkx as nx
import pylab as plt
from graphviz import Digraph, Graph
 
dot = Digraph(name='tree', node_attr={'shape': 'circle'})
try:
    mydb = mysql.connector.connect(
        host="hypegenai.com",
        user="hypegena",
        password="aZ5xjXf133",
        database="hypegena_chain"
    )
    
    mycursor2 = mydb.cursor(buffered=True)
    mycursor3 = mydb.cursor(buffered=True)
except Exception as e:
    print(e)



mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM users2 WHERE atanan_ref LIKE '"+str("a1")+"%"+ "'   ORDER BY atanan_ref ASC  LIMIT 3")
G=nx.Graph()
myresult = mycursor.fetchall()
array_2_lenth= []
array_3_lenth= []
array_4_lenth= []
for i in myresult:
    # print(i[7])
    if len(i[7])>2:
        array_2_lenth.append(i[7])

# print(array_2_lenth)
for i in range(len(array_2_lenth)):
    G.add_edge("a1", ""+array_2_lenth[i]+"")
###################################################################



ilk_ref= array_2_lenth[0]
ikinci_ref=array_2_lenth[1]

###############################3


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM users2 WHERE atanan_ref LIKE '"+str(ikinci_ref)+"%"+ "'   ORDER BY atanan_ref ASC  LIMIT 3")

myresult = mycursor.fetchall()

for i in myresult:
    

    if len(i[7])>3:
        array_3_lenth.append(i[7])
    


# print(array_3_lenth)

for i in range(len(array_3_lenth)):
    G.add_edge(str(ikinci_ref), ""+array_3_lenth[i]+"")

######################################################################

# mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM users2 WHERE atanan_ref LIKE '"+str(ilk_ref)+"%"+ "'   ORDER BY atanan_ref ASC  LIMIT 3")

# myresult = mycursor.fetchall()

# for i in myresult:
    
#     print(i[7])
#     if len(i[7])>3:
#         array_4_lenth.append(i[7])


# for i in range(len(array_4_lenth)):
#     G.add_edge(str(ilk_ref), ""+array_4_lenth[i]+"")



# # Add nodes and edges
# G.add_edge("Halit", "Emre")
# G.add_edge("Halit", "Ali")
# G.add_edge("Ali", "Yusuf")
# G.add_edge("Ali", "Mustafa")
# G.add_edge("Emre", "X")
# G.add_edge("Emre", "Kasım")
# G.add_edge("X", "Murat")
nx.draw(G, with_labels = True)
plt.savefig('labels.png')