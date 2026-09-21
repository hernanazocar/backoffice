"""
Sistema de gestión y aprobación de posts generados por agentes
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# Importar integraciones
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from integrations.social_media import SocialMediaPublisher, MockSocialMediaPublisher
from integrations.design_ai import DesignGenerator, MockDesignGenerator


class PostManager:
    """Gestiona el ciclo de vida completo de los posts"""

    def __init__(self, mock_mode=True):
        """
        Args:
            mock_mode: Si True, usa versiones mock de las APIs (para testing)
        """
        self.mock_mode = mock_mode

        # Inicializar integraciones
        if mock_mode:
            self.social_publisher = MockSocialMediaPublisher()
            self.design_generator = MockDesignGenerator()
        else:
            self.social_publisher = SocialMediaPublisher()
            self.design_generator = DesignGenerator()

        # Directorios
        self.posts_dir = Path('/Users/hernanazocar/developers/agentes-org/posts')
        self.pending_dir = self.posts_dir / 'pending'
        self.approved_dir = self.posts_dir / 'approved'
        self.published_dir = self.posts_dir / 'published'
        self.rejected_dir = self.posts_dir / 'rejected'

        # Crear directorios si no existen
        for dir in [self.pending_dir, self.approved_dir, self.published_dir, self.rejected_dir]:
            dir.mkdir(parents=True, exist_ok=True)

    def get_pending_posts(self) -> List[Dict]:
        """
        Obtiene todos los posts pendientes de aprobación

        Returns:
            Lista de posts con toda su información
        """
        pending_posts = []

        for post_file in self.pending_dir.glob('*.json'):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post_data = json.load(f)
                    post_data['file_path'] = str(post_file)
                    pending_posts.append(post_data)
            except Exception as e:
                print(f"Error leyendo {post_file}: {e}")

        # Ordenar por fecha de creación
        pending_posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        return pending_posts

    def approve_post(self, post_id: str) -> Dict:
        """
        Aprueba un post y lo procesa para publicación

        Steps:
        1. Generar diseño si es necesario
        2. Publicar en la plataforma correspondiente
        3. Mover a approved/published
        4. Retornar resultado

        Args:
            post_id: ID del post a aprobar

        Returns:
            Dict con resultado de la operación
        """
        # Buscar el post
        post_file = self.pending_dir / f'{post_id}.json'

        if not post_file.exists():
            return {
                'success': False,
                'error': f'Post {post_id} not found'
            }

        # Leer datos del post
        with open(post_file, 'r', encoding='utf-8') as f:
            post_data = json.load(f)

        results = []

        # 1. Generar diseño si es necesario
        if post_data.get('needs_design', True) and not post_data.get('image_url'):
            print(f"Generando diseño para post {post_id}...")

            design_spec = post_data.get('design_spec', {})
            design_spec['post_id'] = post_id

            design_result = self.design_generator.generate_social_post_design(design_spec)

            if design_result['success']:
                post_data['image_url'] = design_result['image_url']
                post_data['image_local_path'] = design_result.get('local_path')
                post_data['design_prompt'] = design_result.get('prompt_used')
                print(f"✓ Diseño generado: {design_result['image_url']}")
            else:
                return {
                    'success': False,
                    'error': f"Failed to generate design: {design_result.get('error')}"
                }

        # 2. Publicar en plataforma(s)
        platforms = post_data.get('platforms', ['instagram'])
        copy = post_data.get('copy', '')
        image_url = post_data.get('image_url', '')
        schedule_time = post_data.get('schedule_time')

        for platform in platforms:
            print(f"Publicando en {platform}...")

            if platform == 'instagram':
                result = self.social_publisher.publish_to_instagram(
                    copy=copy,
                    image_url=image_url,
                    schedule_time=schedule_time
                )
            elif platform == 'facebook':
                result = self.social_publisher.publish_to_facebook(
                    copy=copy,
                    image_url=image_url,
                    schedule_time=schedule_time
                )
            elif platform == 'linkedin':
                result = self.social_publisher.publish_to_linkedin(
                    copy=copy,
                    image_url=image_url
                )
            else:
                result = {
                    'success': False,
                    'error': f'Platform {platform} not supported'
                }

            results.append(result)

            if result['success']:
                print(f"✓ Publicado en {platform}: {result.get('post_id')}")
            else:
                print(f"✗ Error en {platform}: {result.get('error')}")

        # 3. Actualizar metadata del post
        post_data['status'] = 'published'
        post_data['approved_at'] = datetime.now().isoformat()
        post_data['publish_results'] = results

        # 4. Mover a published
        published_file = self.published_dir / f'{post_id}.json'

        with open(published_file, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)

        # Eliminar de pending
        post_file.unlink()

        # Determinar éxito general
        all_success = all(r.get('success', False) for r in results)

        return {
            'success': all_success,
            'post_id': post_id,
            'platforms': platforms,
            'results': results,
            'image_url': post_data.get('image_url'),
            'scheduled': bool(schedule_time)
        }

    def reject_post(self, post_id: str, reason: str = '') -> Dict:
        """
        Rechaza un post
        """
        post_file = self.pending_dir / f'{post_id}.json'

        if not post_file.exists():
            return {
                'success': False,
                'error': f'Post {post_id} not found'
            }

        # Leer y actualizar
        with open(post_file, 'r', encoding='utf-8') as f:
            post_data = json.load(f)

        post_data['status'] = 'rejected'
        post_data['rejected_at'] = datetime.now().isoformat()
        post_data['reject_reason'] = reason

        # Mover a rejected
        rejected_file = self.rejected_dir / f'{post_id}.json'

        with open(rejected_file, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)

        post_file.unlink()

        return {
            'success': True,
            'post_id': post_id,
            'status': 'rejected'
        }

    def edit_post(self, post_id: str, updates: Dict) -> Dict:
        """
        Edita un post pendiente
        """
        post_file = self.pending_dir / f'{post_id}.json'

        if not post_file.exists():
            return {
                'success': False,
                'error': f'Post {post_id} not found'
            }

        # Leer datos actuales
        with open(post_file, 'r', encoding='utf-8') as f:
            post_data = json.load(f)

        # Aplicar actualizaciones
        post_data.update(updates)
        post_data['updated_at'] = datetime.now().isoformat()

        # Guardar
        with open(post_file, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)

        return {
            'success': True,
            'post_id': post_id,
            'updated_fields': list(updates.keys())
        }

    def get_published_posts(self, limit: int = 50) -> List[Dict]:
        """
        Obtiene posts ya publicados
        """
        published_posts = []

        for post_file in self.published_dir.glob('*.json'):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post_data = json.load(f)
                    published_posts.append(post_data)
            except Exception as e:
                print(f"Error leyendo {post_file}: {e}")

        # Ordenar por fecha de publicación
        published_posts.sort(key=lambda x: x.get('approved_at', ''), reverse=True)

        return published_posts[:limit]

    def get_post_analytics(self, post_id: str) -> Dict:
        """
        Obtiene analíticas de un post publicado
        """
        post_file = self.published_dir / f'{post_id}.json'

        if not post_file.exists():
            return {
                'success': False,
                'error': 'Post not found or not published'
            }

        with open(post_file, 'r', encoding='utf-8') as f:
            post_data = json.load(f)

        # Obtener métricas de cada plataforma
        analytics = {}

        for result in post_data.get('publish_results', []):
            if result.get('success'):
                platform = result['platform']
                platform_post_id = result['post_id']

                metrics = self.social_publisher.get_post_analytics(platform, platform_post_id)
                analytics[platform] = metrics

        return {
            'success': True,
            'post_id': post_id,
            'analytics': analytics
        }

    def create_post(self, post_data: Dict) -> str:
        """
        Crea un nuevo post pendiente
        Usado por los agentes para crear posts

        Args:
            post_data: Datos del post
                {
                    'copy': 'Texto del post',
                    'platforms': ['instagram', 'facebook'],
                    'schedule_time': '2026-09-22T19:00:00',
                    'hashtags': ['marketing', 'tips'],
                    'needs_design': True,
                    'design_spec': {...}
                }

        Returns:
            post_id generado
        """
        # Generar ID único
        post_id = f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Agregar metadata
        post_data['post_id'] = post_id
        post_data['created_at'] = datetime.now().isoformat()
        post_data['status'] = 'pending'
        post_data['created_by'] = post_data.get('created_by', 'community-manager')

        # Guardar en pending
        post_file = self.pending_dir / f'{post_id}.json'

        with open(post_file, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Post creado: {post_id}")

        return post_id


# Ejemplo de uso
if __name__ == '__main__':
    # Modo de prueba
    manager = PostManager(mock_mode=True)

    # Crear un post de ejemplo
    post_data = {
        'copy': '🚀 ¿Sabías que el 80% de las empresas no aprovechan todo el potencial de las redes sociales? Descubre cómo maximizar tu presencia digital #marketing #tips #negocio',
        'platforms': ['instagram', 'facebook'],
        'schedule_time': '2026-09-22T19:00:00',
        'hashtags': ['marketing', 'tips', 'negocio'],
        'needs_design': True,
        'design_spec': {
            'concept': 'Diseño moderno con gradiente',
            'colors': ['#FF6B35', '#EC4899'],
            'style': 'modern minimalist',
            'layout': 'centered',
            'format': 'instagram_post'
        }
    }

    # Crear post
    post_id = manager.create_post(post_data)

    # Listar pendientes
    print("\nPosts pendientes:")
    pending = manager.get_pending_posts()
    print(f"Total: {len(pending)}")

    # Aprobar el post
    print(f"\nAprobando post {post_id}...")
    result = manager.approve_post(post_id)

    if result['success']:
        print("✓ Post aprobado y publicado exitosamente!")
        print(json.dumps(result, indent=2))
    else:
        print(f"✗ Error: {result.get('error')}")
