from flask import Flask, request, redirect, jsonify
app = Flask(__name__)

@app.get('/')
async def index():
    return jsonify({ 'result': 'Welcome to Flask WebPage' })

@app.get('/param')
async def param():
    params = dict(request.args)
    return jsonify({ 'params': params })

@app.post('/param')
async def posted():
    params = dict(request.form)
    return jsonify({ 'posted': params })

@app.get('/headers')
async def header():
    headers = dict(request.headers)
    return jsonify({ 'headers': headers })

@app.get('/lost')
async def lost():
    return redirect('/')

app.run(
    host='localhost',
    port=5052,
    debug=False
)