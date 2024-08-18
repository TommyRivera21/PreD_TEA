import random
import json
import os
from app.config import Config

# Definición de las preguntas y respuestas
questions = [
    "¿Tu hijo te mira cuando lo llamas por su nombre?",
    "¿Es fácil es para usted establecer contacto visual con su hijo?",
    "¿Su hijo señala para indicar que quiere algo? (por ejemplo, un juguete que está fuera de su alcance)",
    "¿Su hijo finge? (por ejemplo, cuidar muñecas, hablar por un teléfono de juguete)?",
    "¿Su hijo finge? (por ejemplo, cuidar muñecas, hablar por un teléfono de juguete)",
    "¿Su hijo sigue hacia donde usted mira?",
    "¿Si usted o alguien más en la familia está visiblemente molesto, ¿su hijo muestra signos de querer consolarlo? (por ejemplo, acariciar el cabello, abrazarlos)",
    "¿Su hijo utilizó palabras de manera coherente durante sus primeras etapas del habla?",
    "¿Su hijo utiliza gestos sencillos? (por ejemplo, decir adiós)",
    "¿Su hijo mira fijamente a la nada sin ningún propósito aparente?",
    "¿Su hijo(a) parece no notar el dolor o la temperatura de manera adecuada?",
    "¿Su hijo(a) tiene un desarrollo del lenguaje retrasado en comparación con otros niños de su edad?",
    "¿Su hijo(a) repite palabras o frases de manera repetitiva (ecolalia)?",
    "¿Su hijo(a) usa frases y oraciones que no parecen tener sentido en el contexto?",
    "¿Su hijo(a) participa en juegos de simulación o juego imaginativo (por ejemplo, jugar a la casita, hacer de cuenta que es un superhéroe)?",
    "¿Su hijo(a) se interesa en los juguetes de manera típica para su edad (por ejemplo, usar bloques para construir en lugar de solo alinearlos)?",
    "¿Su hijo(a) comparte intereses con otros niños (por ejemplo, muestra un juguete a otro niño para que lo vea)?",
    "¿Su hijo(a) muestra torpeza o falta de coordinación motora?",
    "¿Su hijo(a) tiene dificultades para aprender nuevas habilidades motoras (por ejemplo, andar en bicicleta, atarse los zapatos)?",
    "¿Su hijo(a) tiene dificultades para mantener la atención en actividades o tareas?",
    "¿Su hijo(a) parece hiperactivo(a) o tiene mucha energía?",
    "¿Su hijo(a) inicia la interacción con compañeros o adultos (por ejemplo, iniciar una conversación, pedir jugar)?",
    "¿Su hijo(a) se altera extremadamente por cambios menores o transiciones (por ejemplo, cambiar una rutina, ir a un lugar nuevo)?",
    "¿Su hijo(a) tiene intereses intensos y enfocados que son inusuales en intensidad o enfoque (por ejemplo, un interés intenso en un tema u objeto específico)?",
    "¿Su hijo(a) mira fijamente a un objeto o a un punto fijo sin un propósito aparente?",
    "¿Su hijo(a) utiliza frases cotidianas para comunicarse, como hola o adiós?",
    "¿Su hijo(a) usa su mirada para seguir la dirección en la que usted está mirando?",
    "¿Su hijo(a) mira hacia usted cuando dice su nombre?",
    "¿Su hijo(a) muestra interés en compartir experiencias con usted, por ejemplo, señalando un lugar que le llama la atención?",
    "¿Su hijo(a) muestra signos de consuelo, como acariciar o abrazar a alguien cuando está visiblemente molesto?"
]

answers = ["Siempre", "Generalmente", "A veces", "Rara vez", "Nunca"]

# Ruta para guardar los datos generados
save_path = Config.GENERATION_QUESTIONNAIRE_TRAINING_DATA_DIR

# Crear directorio si no existe
os.makedirs(save_path, exist_ok=True)

# Generar datos sintéticos
def generate_synthetic_data(num_samples=50000):
    data = []
    for _ in range(num_samples):
        sample = [{"question": question, "answer": random.choice(answers)} for question in questions]
        data.append(sample)

    # Guardar los datos generados en un archivo JSON
    file_name = os.path.join(save_path, "training_data.json")
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Datos sintéticos guardados en {file_name}")

# Ejecutar la generación de datos
if __name__ == "__main__":
    generate_synthetic_data()
