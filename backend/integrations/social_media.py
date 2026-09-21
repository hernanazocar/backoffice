"""
Integración con APIs de Redes Sociales
"""

import os
import requests
from datetime import datetime
from typing import Dict, Optional
import json

class SocialMediaPublisher:
    """Publica contenido en diferentes redes sociales"""

    def __init__(self):
        self.meta_token = os.getenv('META_ACCESS_TOKEN')
        self.meta_page_id = os.getenv('META_PAGE_ID')
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_org_id = os.getenv('LINKEDIN_ORG_ID')

    def publish_to_instagram(self, copy: str, image_url: str, schedule_time: Optional[str] = None) -> Dict:
        """
        Publica en Instagram usando Meta Graph API

        Args:
            copy: Texto del post
            image_url: URL de la imagen
            schedule_time: Opcional - Fecha/hora para programar (ISO format)

        Returns:
            Dict con el resultado de la publicación
        """
        if not self.meta_token or not self.meta_page_id:
            return {
                'success': False,
                'error': 'Meta credentials not configured',
                'platform': 'instagram'
            }

        url = f"https://graph.facebook.com/v18.0/{self.meta_page_id}/photos"

        params = {
            'access_token': self.meta_token,
            'url': image_url,
            'caption': copy,
        }

        # Si hay schedule_time, programar en lugar de publicar
        if schedule_time:
            params['published'] = False
            params['scheduled_publish_time'] = self._convert_to_unix(schedule_time)
        else:
            params['published'] = True

        try:
            response = requests.post(url, params=params)
            data = response.json()

            if response.status_code == 200:
                return {
                    'success': True,
                    'post_id': data.get('id'),
                    'platform': 'instagram',
                    'scheduled': bool(schedule_time),
                    'schedule_time': schedule_time
                }
            else:
                return {
                    'success': False,
                    'error': data.get('error', {}).get('message', 'Unknown error'),
                    'platform': 'instagram'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'platform': 'instagram'
            }

    def publish_to_facebook(self, copy: str, image_url: str, schedule_time: Optional[str] = None) -> Dict:
        """
        Publica en Facebook Page usando Meta Graph API
        """
        if not self.meta_token or not self.meta_page_id:
            return {
                'success': False,
                'error': 'Meta credentials not configured',
                'platform': 'facebook'
            }

        url = f"https://graph.facebook.com/v18.0/{self.meta_page_id}/photos"

        params = {
            'access_token': self.meta_token,
            'url': image_url,
            'message': copy,
        }

        if schedule_time:
            params['published'] = False
            params['scheduled_publish_time'] = self._convert_to_unix(schedule_time)
        else:
            params['published'] = True

        try:
            response = requests.post(url, params=params)
            data = response.json()

            if response.status_code == 200:
                return {
                    'success': True,
                    'post_id': data.get('id'),
                    'platform': 'facebook',
                    'scheduled': bool(schedule_time),
                    'schedule_time': schedule_time
                }
            else:
                return {
                    'success': False,
                    'error': data.get('error', {}).get('message', 'Unknown error'),
                    'platform': 'facebook'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'platform': 'facebook'
            }

    def publish_to_linkedin(self, copy: str, image_url: str) -> Dict:
        """
        Publica en LinkedIn usando LinkedIn API
        """
        if not self.linkedin_token or not self.linkedin_org_id:
            return {
                'success': False,
                'error': 'LinkedIn credentials not configured',
                'platform': 'linkedin'
            }

        url = "https://api.linkedin.com/v2/ugcPosts"

        headers = {
            'Authorization': f'Bearer {self.linkedin_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        # Primero subir la imagen
        asset = self._upload_linkedin_image(image_url)

        if not asset:
            return {
                'success': False,
                'error': 'Failed to upload image to LinkedIn',
                'platform': 'linkedin'
            }

        payload = {
            "author": f"urn:li:organization:{self.linkedin_org_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": copy
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()

            if response.status_code == 201:
                return {
                    'success': True,
                    'post_id': data.get('id'),
                    'platform': 'linkedin'
                }
            else:
                return {
                    'success': False,
                    'error': data.get('message', 'Unknown error'),
                    'platform': 'linkedin'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'platform': 'linkedin'
            }

    def _upload_linkedin_image(self, image_url: str) -> Optional[str]:
        """Sube una imagen a LinkedIn y retorna el URN del asset"""
        # Implementación simplificada
        # En producción, debes seguir el flujo completo de LinkedIn para subir imágenes
        return None

    def _convert_to_unix(self, iso_datetime: str) -> int:
        """Convierte datetime ISO a timestamp Unix"""
        dt = datetime.fromisoformat(iso_datetime)
        return int(dt.timestamp())

    def get_post_analytics(self, platform: str, post_id: str) -> Dict:
        """
        Obtiene analíticas de un post publicado
        """
        if platform == 'instagram':
            return self._get_instagram_analytics(post_id)
        elif platform == 'facebook':
            return self._get_facebook_analytics(post_id)
        elif platform == 'linkedin':
            return self._get_linkedin_analytics(post_id)
        else:
            return {'error': 'Platform not supported'}

    def _get_instagram_analytics(self, post_id: str) -> Dict:
        """Obtiene métricas de un post de Instagram"""
        url = f"https://graph.facebook.com/v18.0/{post_id}?fields=like_count,comments_count,insights.metric(reach,impressions,engagement)&access_token={self.meta_token}"

        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def _get_facebook_analytics(self, post_id: str) -> Dict:
        """Obtiene métricas de un post de Facebook"""
        # Similar a Instagram
        return {}

    def _get_linkedin_analytics(self, post_id: str) -> Dict:
        """Obtiene métricas de un post de LinkedIn"""
        # Implementar según API de LinkedIn
        return {}


# Modo de prueba sin credenciales
class MockSocialMediaPublisher(SocialMediaPublisher):
    """Versión de prueba que simula publicaciones sin APIs reales"""

    def __init__(self):
        pass

    def publish_to_instagram(self, copy: str, image_url: str, schedule_time: Optional[str] = None) -> Dict:
        print(f"[MOCK] Publicando en Instagram:")
        print(f"  Copy: {copy[:50]}...")
        print(f"  Imagen: {image_url}")
        print(f"  Programado: {schedule_time or 'Ahora'}")

        return {
            'success': True,
            'post_id': f'mock_ig_{datetime.now().timestamp()}',
            'platform': 'instagram',
            'scheduled': bool(schedule_time),
            'schedule_time': schedule_time,
            'mode': 'mock'
        }

    def publish_to_facebook(self, copy: str, image_url: str, schedule_time: Optional[str] = None) -> Dict:
        print(f"[MOCK] Publicando en Facebook:")
        print(f"  Copy: {copy[:50]}...")

        return {
            'success': True,
            'post_id': f'mock_fb_{datetime.now().timestamp()}',
            'platform': 'facebook',
            'mode': 'mock'
        }

    def publish_to_linkedin(self, copy: str, image_url: str) -> Dict:
        print(f"[MOCK] Publicando en LinkedIn:")
        print(f"  Copy: {copy[:50]}...")

        return {
            'success': True,
            'post_id': f'mock_li_{datetime.now().timestamp()}',
            'platform': 'linkedin',
            'mode': 'mock'
        }
