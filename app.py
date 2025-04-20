from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from time import sleep
from datetime import datetime
import os
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config['SCHEDULER_API_ENABLED'] = True  # Opcional: habilita una API para gestionar los jobs
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
programaciones = {}

# Cargar programaciones al iniciar la aplicación
def cargar_programaciones():
    global programaciones
    try:
        if os.path.exists('programaciones.json'):
            with open('programaciones.json', 'r') as f:
                programaciones_str = json.load(f)
                # Convertir fechas de string a objetos datetime
                for receta_id, fecha_str in programaciones_str.items():
                    programaciones[int(receta_id)] = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                print(f"Programaciones cargadas: {programaciones}")
    except Exception as e:
        print(f"Error al cargar programaciones: {e}")
        programaciones = {}

# Guardar programaciones en archivo
def guardar_programaciones_archivo():
    global programaciones
    try:
        # Convertir datetime a string para poder serializar a JSON
        programaciones_str = {receta_id: fecha.strftime('%Y-%m-%d %H:%M:%S') 
                             for receta_id, fecha in programaciones.items()}
        with open('programaciones.json', 'w') as f:
            json.dump(programaciones_str, f, indent=2)
        print(f"Programaciones guardadas en archivo: {programaciones_str}")
    except Exception as e:
        print(f"Error al guardar programaciones: {e}")

# Cargar programaciones al inicio
cargar_programaciones()

@app.route('/')
def index():
    with open('recetas.json', 'r') as f:
        recetas = json.load(f)
    return render_template('index.html', recetas=recetas)

@app.route('/dashboard')
def dashboard():
    """Dashboard para mostrar las programaciones actuales"""
    global programaciones
    
    # Cargar recetas para mostrar nombres en lugar de IDs
    with open('recetas.json', 'r') as f:
        recetas = json.load(f)
    
    # Formatear programaciones para la vista
    programaciones_formateadas = []
    for receta_id, fecha in programaciones.items():
        # Convertir receta_id a entero si es string
        receta_id_int = int(receta_id) if isinstance(receta_id, str) else receta_id
        
        # Buscar la receta correspondiente
        receta = next((r for r in recetas if r['id'] == receta_id_int), None)
        
        if receta:
            programaciones_formateadas.append({
                'id': receta_id_int,
                'nombre': receta['nombre'],
                'fecha_programada': fecha.strftime('%Y-%m-%d %H:%M'),
                'tiempo_coccion': f"{receta['tiempo']} {receta['unidad_tiempo']}"
            })
    
    return render_template('dashboard.html', programaciones=programaciones_formateadas)

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
            
            # Simulamos la cocción en el servidor
            # En lugar de bloquear con sleep, respondemos inmediatamente
            # y dejamos que el cliente simule el progreso
            # sleep(tiempo_coccion)
            
            mensaje_final = f"¡Cocción de '{nombre_receta}' finalizada!"
            return jsonify({
                'mensaje': mensaje, 
                'mensaje_final': mensaje_final, 
                'receta': nombre_receta,
                'tiempo': tiempo_coccion,
                'unidad_tiempo': unidad_tiempo
            })
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

        mensaje = f"Receta con ID {receta_id} personalizada. Nuevo tiempo: {nuevo_tiempo}."
        return redirect(url_for('personalizar_receta', receta_id=receta_id, mensaje=mensaje))
    else:
        return "Método no permitido.", 405

def iniciar_coccion_programada(receta_id):
    """Función que simula el inicio de la cocción programada"""
    try:
        with open('recetas.json', 'r') as f:
            recetas = json.load(f)
            
        receta = next((r for r in recetas if r['id'] == receta_id), None)
        if receta:
            nombre_receta = receta['nombre']
            tiempo = receta.get('tiempo', 0)
            print(f"[PROGRAMACIÓN] Iniciando cocción de '{nombre_receta}' por {tiempo} minutos")
            # Aquí simularíamos la cocción en un entorno real
            # En este caso no usamos sleep porque bloquearía el scheduler
            return True
        else:
            print(f"[PROGRAMACIÓN] No se encontró la receta con ID {receta_id}")
            return False
    except Exception as e:
        print(f"[PROGRAMACIÓN] Error al iniciar cocción: {e}")
        return False

def verificar_programaciones():
    global programaciones
    ahora = datetime.now()
    print(f"[{ahora}] Verificando programaciones...")
    programaciones_a_eliminar = []
    
    if not programaciones:
        print(f"[{ahora}] No hay programaciones pendientes.")
        return
        
    print(f"[{ahora}] Programaciones actuales: {programaciones}")
    
    for receta_id_str, hora_programada in list(programaciones.items()):
        # Asegurar que receta_id sea entero
        receta_id = int(receta_id_str) if isinstance(receta_id_str, str) else receta_id_str
        
        print(f"[{ahora}] Revisando receta ID {receta_id} programada para: {hora_programada}")
        
        # Comparar fechas
        if ahora >= hora_programada:
            print(f"[{ahora}] ¡Hora alcanzada! Iniciando cocción programada para la receta ID {receta_id}")
            # Iniciar la cocción
            if iniciar_coccion_programada(receta_id):
                # Añadir a la lista para eliminar después
                programaciones_a_eliminar.append(receta_id)
            else:
                print(f"[{ahora}] Error al iniciar cocción de receta ID {receta_id}")
    
    # Eliminar programaciones ejecutadas
    for receta_id in programaciones_a_eliminar:
        if receta_id in programaciones:
            del programaciones[receta_id]
            print(f"[{ahora}] Programación para receta ID {receta_id} eliminada")
    
    # Guardar las programaciones restantes
    if programaciones_a_eliminar:
        guardar_programaciones_archivo()

@app.route('/guardar_programacion/<int:receta_id>', methods=['POST'])
def guardar_programacion(receta_id):
    global programaciones
    print(f"Estado de programaciones antes de guardar: {programaciones}")

    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        hora_str = request.form.get('hora')

        if fecha_str and hora_str:
            try:
                programar_en_str = f"{fecha_str} {hora_str}"
                programar_en = datetime.strptime(programar_en_str, '%Y-%m-%d %H:%M')

                # Guardar en programaciones
                programaciones[receta_id] = programar_en

                # Guardar en archivo para persistencia
                guardar_programaciones_archivo()

                print(f"Programación guardada: {programaciones}")
                mensaje = f"Cocción de la receta con ID {receta_id} programada para {programar_en_str}."
                return redirect(url_for('index', mensaje_programacion=mensaje))
            except ValueError as e:
                print(f"Error al guardar programación: {e}")
                return "Formato de fecha u hora inválido.", 400
        else:
            return "Por favor, seleccione fecha y hora.", 400
    else:
        return "Método no permitido.", 405

# Programar la tarea de verificación para que se ejecute cada minuto
scheduler.add_job(id='verificar_programaciones', func=verificar_programaciones, trigger='interval', seconds=30)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)