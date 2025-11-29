import pika
import json
from tika import parser

# Configuration RabbitMQ
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'raw_documents_queue'

def extract_text_from_file(file_path: str):
    """Envoie le fichier au serveur Tika (port 9998) pour extraire le texte"""
    try:
        # Tika détecte automatiquement si c'est un PDF, Docx, etc.
        # On utilise le serveur Tika dockerisé
        parsed = parser.from_file(file_path, serverEndpoint='http://localhost:9998/tika')
        return parsed.get("content", "").strip()
    except Exception as e:
        print(f"Erreur Tika: {e}")
        return None

def publish_to_queue(doc_id: int, text: str, metadata: dict):
    """Envoie le JSON dans RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    
    # On s'assure que la queue existe
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
    message = {
        "doc_id": doc_id,
        "text": text,
        "metadata": metadata
    }
    
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Rend le message persistant (ne se perd pas si RabbitMQ crash)
        )
    )
    print(f" [x] Envoyé document ID {doc_id} vers RabbitMQ")
    connection.close()