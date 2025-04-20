from flask import Flask, render_template, request, jsonify
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
    with open('recetas.json', 'r') as f:
        recetas = json.load(f)
        
        receta_seleccionada = next((receta for receta in recetas if receta['id'] == receta_id), None)
        
        if receta_seleccionada:
            nombre_receta = receta_seleccionada['nombre']
            tiempo_coccion = receta_seleccionada.get('tiempo', 0) # Usamos .get() con un valor por defecto
            unidad_tiempo = receta_seleccionada.get('unidad_tiempo', 'minutos') # Aseguramos tener un valor
            
            mensaje = f"Receta '{nombre_receta}' enviada al horno. " \
                      f"Simulando cocción por {tiempo_coccion} {unidad_tiempo}..."
            
            sleep(tiempo_coccion)
            
            mensaje_final = f"¡Cocción de '{nombre_receta}' finalizada!"
            return jsonify({'mensaje': mensaje, 'mensaje_final': mensaje_final, 'receta': nombre_receta})
        else:
            return jsonify({'error': f'No se encontró la receta con ID {receta_id}'}), 404

@app.route('/personalizar_receta/<int:receta_id>')
def personalizar_receta(receta_id):
    with open('recetas.json', 'r') as f:
        recetas = json.load(f)
        
        receta_a_personalizar = next((receta for receta in recetas if receta['id'] == receta_id), None)
        
        if receta_a_personalizar:
            return render_template('personalizar.html', receta=receta_a_personalizar)
        else:
            return "receta no encontrada.", 404

@app.route('/guardar_personalizacion/<int:receta_id>', methods=['POST'])
def guardar_personalizacion(receta_id):
    if request.method == 'POST':
        nuevo_tiempo = request.form.get('tiempo')
        # Aquí podríamos obtener otros parámetros de personalización en el futuro
        
        with open('recetas.json', 'r+') as f:
            recetas = json.load(f)
            for receta in recetas:
                if receta['id'] == receta_id:
                    receta['tiempo'] = int(nuevo_tiempo) if nuevo_tiempo else receta['tiempo']
                    # Aqui podríamos actualizar otros parámetros también
            
            f.seek(0)
            json.dump(recetas, f, indent=2)
            f.truncate()
        
        return f"receta con ID {receta_id} personalizada. Nuevo tiempo: {nuevo_tiempo}."
    else:
        return "Método no permitido.", 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)