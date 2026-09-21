"""
API REST para gestión de posts de marketing
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Agregar path del backend
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from approval_system.post_manager import PostManager

app = Flask(__name__)
CORS(app)  # Permitir requests desde el dashboard

# Inicializar PostManager en modo mock por defecto
# Cambiar a mock_mode=False cuando tengas las credenciales configuradas
post_manager = PostManager(mock_mode=True)


@app.route('/api/marketing/posts/pending', methods=['GET'])
def get_pending_posts():
    """Obtiene todos los posts pendientes de aprobación"""
    try:
        posts = post_manager.get_pending_posts()
        return jsonify({
            'success': True,
            'count': len(posts),
            'posts': posts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketing/posts/published', methods=['GET'])
def get_published_posts():
    """Obtiene posts ya publicados"""
    try:
        limit = request.args.get('limit', 50, type=int)
        posts = post_manager.get_published_posts(limit=limit)
        return jsonify({
            'success': True,
            'count': len(posts),
            'posts': posts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketing/posts/<post_id>/approve', methods=['POST'])
def approve_post(post_id):
    """Aprueba y publica un post"""
    try:
        result = post_manager.approve_post(post_id)

        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketing/posts/<post_id>/reject', methods=['POST'])
def reject_post(post_id):
    """Rechaza un post"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', '')

        result = post_manager.reject_post(post_id, reason)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketing/posts/<post_id>/edit', methods=['PUT'])
def edit_post(post_id):
    """Edita un post pendiente"""
    try:
        updates = request.get_json()

        if not updates:
            return jsonify({
                'success': False,
                'error': 'No updates provided'
            }), 400

        result = post_manager.edit_post(post_id, updates)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketing/posts/create', methods=['POST'])
def create_post():
    """Crea un nuevo post (usado por agentes)"""
    try:
        post_data = request.get_json()

        if not post_data:
            return jsonify({
                'success': False,
                'error': 'No post data provided'
            }), 400

        post_id = post_manager.create_post(post_data)

        return jsonify({
            'success': True,
            'post_id': post_id
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketing/posts/<post_id>/analytics', methods=['GET'])
def get_post_analytics(post_id):
    """Obtiene analíticas de un post publicado"""
    try:
        result = post_manager.get_post_analytics(post_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketing/status', methods=['GET'])
def get_status():
    """Estado general del sistema de marketing"""
    try:
        pending = post_manager.get_pending_posts()
        published = post_manager.get_published_posts(limit=10)

        return jsonify({
            'success': True,
            'status': 'operational',
            'mock_mode': post_manager.mock_mode,
            'pending_count': len(pending),
            'recent_published_count': len(published)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/marketing/execute-workflow', methods=['POST'])
def execute_workflow():
    """Ejecuta el workflow completo de marketing (todos los agentes)"""
    try:
        import subprocess
        import threading

        # Ejecutar workflow en background
        def run_workflow():
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ejecutar_workflow.py')
            venv_python = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'venv', 'bin', 'python3')

            # Si existe el venv, usarlo
            python_cmd = venv_python if os.path.exists(venv_python) else 'python3'

            subprocess.run([python_cmd, script_path, 'marketing'],
                          cwd=os.path.dirname(os.path.dirname(__file__)))

        # Iniciar en thread separado para no bloquear
        thread = threading.Thread(target=run_workflow)
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'message': 'Workflow de marketing iniciado',
            'status': 'running',
            'estimated_time': '2-3 minutos'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Marketing API iniciada")
    print("📍 Endpoints disponibles:")
    print("   GET  /api/marketing/posts/pending")
    print("   GET  /api/marketing/posts/published")
    print("   POST /api/marketing/posts/<id>/approve")
    print("   POST /api/marketing/posts/<id>/reject")
    print("   PUT  /api/marketing/posts/<id>/edit")
    print("   POST /api/marketing/posts/create")
    print("   GET  /api/marketing/posts/<id>/analytics")
    print("   GET  /api/marketing/status")
    print("   POST /api/marketing/execute-workflow  ← NUEVO: Ejecutar equipo")
    print("\n🌐 Corriendo en http://localhost:5000")

    app.run(debug=True, port=5000)
