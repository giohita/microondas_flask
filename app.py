from flask import Flask, render_template, request, jsonify
import json
from time import sleep
from datetime import datetime

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

programaciones = {}

@app.route('/guardar_programacion/<int:receta_id>', methods=['POST'])
def guardar_programacion(receta_id):
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        hora_str = request.form.get('hora')
        
        if fecha_str and hora_str:
            try:
                programar_en_str = f"{fecha_str} {hora_str}"
                programar_en = datetime.strptime(programar_en_str, '%Y-%m-%d %H:%M')
                programaciones[receta_id] = programar_en
                print(f"Programación guardada: {programaciones}") # Añade esta línea
                return f"Cocción de la receta con ID {receta_id} programada para las {programar_en_str}."
            except ValueError:
                return "Formato de fecha u hora inválido.", 400
        else:
            return "Por favor, seleccione fecha y hora.", 400
    else:
        return "Método no permitido.", 405

#función para simular la verificación de programaciones (esto sería más complejo en una app real)
def verificar_programaciones():
    ahora = datetime.now()
    for receta_id, hora_programada in list(programaciones.items()): # Iterar sobre una copia para permitir la eliminación
        if ahora >= hora_programada:
            print(f"Iniciando cocción programada para la receta con ID {receta_id}")
            # Aquí iría la lógica real para inciar la cocción (simulación)
            del programaciones[receta_id] # Eliminar de las programaciones activas

# Simulación de un proceso en segundo plano para verificar prograaciones (solo para demostración)
import threading
def ejecutar_verificacion_periodica():
    while True:
        verificar_programaciones()
        sleep(60) # Verificar cada 60 segundos

thread = threading.Thread(target=ejecutar_verificacion_periodica)
thread.daemon = True # El hilo Terminará cuando la aplicación principal termine
thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)