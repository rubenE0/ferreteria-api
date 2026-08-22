import requests
from .models import Producto, Marca, Categoria

def consultar_asistente_inventario(pregunta_usuario):

    productos = Producto.objects.all()
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()

    if not productos.exists():
        return "No hay productos en el inventario."

    inf_productos = []
    inf_marcas = []
    inf_categorias = []
    for p in productos:
        inf_productos.append(f"Producto: {p.nombre}| Stock: {p.stock_actual}, Stock Minimo: {p.stock_minimo}, Precio: {p.precio}")
    for m in marcas:
        inf_marcas.append(f"Marca: {m.nombre}")
    for c in categorias:
        inf_categorias.append(f"Categoria: {c.nombre}")

    contexto_inventario = "\n".join(inf_productos + inf_marcas + inf_categorias)


    prompt_ia = f"""
        Eres un asistente virtual especializado en el inventario de una ferretería.
        Ademas tienes la lista actualizada de productos: {contexto_inventario}

        Instrucciones:
        1. Si la pregunta se relaciona con el inventario, productos, stock o precios, responde usando la información que posees y tu conocimiento general sobre ferretería.
        2. Si la pregunta NO tiene nada que ver con la ferretería o el inventario, responde amablemente: "Lo siento, solo puedo responder preguntas relacionadas con el inventario de la ferretería."
        3. Sé directo, conciso y profesional.

        Pregunta del usuario: {pregunta_usuario}
        """
    
    url = "http://localhost:11434/api/generate"
    payload = {
           "model": "deepseek-r1:7b",
            "prompt": prompt_ia,
            "stream": False
        }

    try:
        response = requests.post(url, json=payload, timeout=120)
        if response.status_code == 200:
            resultado = response.json().get("response", "")
            
            if "</think>" in resultado:
                resultado = resultado.split("</think>")[-1].strip()
                
            return resultado
        else:
            return f"Error en Ollama: Código HTTP {response.status_code}"
    except Exception as e:
        return f"Error de conexión con Ollama: {str(e)}"