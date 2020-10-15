'''
Note: Server-side processor for generating and processing encoded audio.
Author: Mansoor Rahimat Khan
Date: 31st Jan 2019
Organization: Tonetag Pvt Ltd
'''



from flask import Flask, render_template, request, redirect, Response, jsonify
import encoding_experimental, decoding_experimental
import ssl
import random, json
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/encode')
def encode():
    bit_coding = request.args.get("data")
    data = encoding_experimental.out_encoded_audio(bit_coding)
    return jsonify(data)


@app.route("/decode", methods = ['POST'])
def decode():
    decoding_experimental.identify_v3_upload()
    print('checkpoint1')
    #tempo = 139.67483108
    tempo = decoding_experimental.find_bpm('/Users/mansoorkhan/ToneTag_Experiments/Python Projects/Environment_detection/Friday_Demo/fast_mansoor4.wav')
    print('checkpoint2')
    tempo_array = decoding_experimental.in_decoded_audio('recorded_encoded_file.wav')
    print('checkpoint3')
    arr = decoding_experimental.assign_binaries(tempo_array,tempo)
    print('arr response: ', arr)
    return jsonify(arr)

def run_local(flask_app, port=5000):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('./ssl_self_signed/cert.crt', './ssl_self_signed/key.key')
    flask_app.run(host='0.0.0.0', debug=True, port=port, ssl_context= ssl_context)


if __name__ == '__main__':
    #app.run(host='localhost',port='5050',debug=True)
    run_local(app)
