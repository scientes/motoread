
import time
import PIL as pil
import pyttsx3 as tts
import sqlite3 as sql
import tensorflow as tf
import numpy as np
import label_image


import argparse
def sqlinit():
    conn=sql.connect("test.db")
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute(
        "CREATE Table if not exists val (Value_type text, value real , unit text,time int, PRIMARY KEY(`Value_type`,`time`));")
    conn.execute(
        "CREATE Table if not exists pic (pic blob,time int);")
    conn.close()
def insert_value(type,value,unit,time):
    conn.execute("INSERT into val  VALUES(?,?,?,?)",(type,value,unit,time))
def insert_pic(file,time):
    conn.execute("INSERT into pic  VALUES(?,?)",(sql.Binary(f),time))
def read_single_letter(file_name):
    model_file = \
    "output_graph.pb"
    label_file = "output_labels.txt"
    input_height = 224
    input_width = 224
    input_mean = 0
    input_std = 255
    input_layer = "input"
    output_layer = "final_result"

    graph = label_image.load_graph(model_file)
    t = label_image.read_tensor_from_image_file(
      file_name,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: t
        })
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = label_image.load_labels(label_file)
    for i in top_k:
        a=labels[i]
        b=a.split(" ")
        print(b)
        return chr(int(b[1]))        
        break
    

def main():
    engine=tts.init("espeak")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', "german")
    engine.say("Willkommen")
    engine.runAndWait()
    print("SQLlite version: "+sql.version)
    sqlinit()
    engine.say(read_single_letter("b2.png"))
    engine.runAndWait()


if __name__ == '__main__':
    main()
