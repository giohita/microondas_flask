from flask import Flask, render_template, jsonify
import json
from time import sleep

app = Flask(__name__)

@app.route('/')
def index():
    with open('recetas.json', 'r') as f:
        recetas = json.load(f)
    return render_template('index.html', recetas=recetas)

@app.route('/enviar_horno/<int:receta_id>')
def enviar_horno(receta_id):
    ''' Aquí recibimos el ID de la receta que se quiere enviar al horno
    Por ahora, vamos a simular el proceso y devolver un mensaje
    '''
    
    with open('recetas.json', 'r') as f:
        recetas = json.load(f)
        
        receta_seleccionada = next((receta for receta in recetas if receta['id'] == receta_id), None)
        
        if receta_seleccionada:
            nombre_receta = receta_seleccionada['nombre']
            tiempo_coccion = receta_seleccionada['tiempo']
            unidad_tiempo = receta_seleccionada['unidad_tiempo']
            
            mensaje = f"Receta '{nombre_receta}' enviada al horno. " \
                      f"Simulando cocción por {tiempo_coccion} {unidad_tiempo}..."
            
            # Simulación de la cocción (puedes ajustar el tiempo para pruebas)
            sleep(tiempo_coccion)
            
            mensaje_final = f"¡Cocción de '{nombre_receta}' finalizada!"
            return jsonify({'mensaje': mensaje, 'mensaje_final': mensaje_final, 'receta': nombre_receta})
        else:
            return jsonify({'error': f'No se encontró la receta con ID {receta_id}'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)