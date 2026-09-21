"""
Generación de diseños con IA (DALL-E, Midjourney, etc.)
"""

import os
import requests
from typing import Dict, Optional
from openai import OpenAI
from datetime import datetime
import json

class DesignGenerator:
    """Genera diseños gráficos usando IA"""

    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if self.openai_key:
            self.client = OpenAI(api_key=self.openai_key)
        else:
            self.client = None

    def generate_social_post_design(self, design_spec: Dict) -> Dict:
        """
        Genera un diseño para post de redes sociales

        Args:
            design_spec: Especificación del diseño
                {
                    "concept": "Descripción del concepto",
                    "colors": ["#FF6B35", "#EC4899"],
                    "style": "modern minimalist",
                    "text_content": "Texto a incluir",
                    "format": "instagram_post",  # o "facebook_cover", etc.
                    "layout": "centered"
                }

        Returns:
            Dict con URL de la imagen generada
        """
        if not self.client:
            return {
                'success': False,
                'error': 'OpenAI API key not configured'
            }

        # Construir prompt optimizado para DALL-E
        prompt = self._build_design_prompt(design_spec)

        # Determinar tamaño según formato
        size = self._get_image_size(design_spec.get('format', 'instagram_post'))

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="hd",
                n=1,
            )

            image_url = response.data[0].url

            # Descargar y guardar la imagen localmente
            local_path = self._download_and_save(image_url, design_spec.get('post_id', 'design'))

            return {
                'success': True,
                'image_url': image_url,
                'local_path': local_path,
                'prompt_used': prompt,
                'model': 'dall-e-3'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _build_design_prompt(self, design_spec: Dict) -> str:
        """
        Construye un prompt optimizado para DALL-E basado en las especificaciones
        """
        concept = design_spec.get('concept', '')
        colors = design_spec.get('colors', [])
        style = design_spec.get('style', 'modern professional')
        text_content = design_spec.get('text_content', '')
        layout = design_spec.get('layout', 'centered')

        # Construir descripción de colores
        color_desc = ""
        if colors:
            if len(colors) == 1:
                color_desc = f"with {colors[0]} as the main color"
            elif len(colors) == 2:
                color_desc = f"with a gradient from {colors[0]} to {colors[1]}"
            else:
                color_desc = f"using colors {', '.join(colors)}"

        # Prompt final
        prompt = f"""
        Create a professional social media post design for Instagram/Facebook.

        Concept: {concept}
        Style: {style}
        Colors: {color_desc}
        Layout: {layout}

        Design requirements:
        - High quality, professional marketing design
        - Clean and modern aesthetic
        - Optimized for social media engagement
        - {layout} composition
        - Suitable for {design_spec.get('format', 'Instagram post')}

        """.strip()

        # Si hay texto específico, añadirlo
        if text_content:
            prompt += f"\n\nInclude this text prominently: \"{text_content}\""

        # Limitar a 4000 caracteres (límite de DALL-E)
        return prompt[:4000]

    def _get_image_size(self, format_type: str) -> str:
        """
        Retorna el tamaño óptimo según el formato
        """
        sizes = {
            'instagram_post': '1024x1024',
            'instagram_story': '1024x1792',
            'facebook_post': '1024x1024',
            'facebook_cover': '1792x1024',
            'linkedin_post': '1024x1024',
            'twitter_post': '1024x1024'
        }

        return sizes.get(format_type, '1024x1024')

    def _download_and_save(self, image_url: str, post_id: str) -> str:
        """
        Descarga la imagen de DALL-E y la guarda localmente
        """
        # Crear directorio si no existe
        today = datetime.now().strftime('%Y-%m-%d')
        save_dir = f'/Users/hernanazocar/developers/agentes-org/assets/marketing/{today}'
        os.makedirs(save_dir, exist_ok=True)

        # Descargar imagen
        response = requests.get(image_url)

        if response.status_code == 200:
            filename = f'{post_id}_{datetime.now().timestamp()}.png'
            filepath = os.path.join(save_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            return filepath
        else:
            return None

    def generate_variations(self, image_url: str, n: int = 2) -> Dict:
        """
        Genera variaciones de un diseño existente
        """
        if not self.client:
            return {
                'success': False,
                'error': 'OpenAI API key not configured'
            }

        try:
            response = self.client.images.create_variation(
                image=open(image_url, "rb"),
                n=n,
                size="1024x1024"
            )

            variations = [img.url for img in response.data]

            return {
                'success': True,
                'variations': variations,
                'count': len(variations)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def edit_design(self, original_image_path: str, edit_prompt: str) -> Dict:
        """
        Edita un diseño existente según instrucciones
        """
        # DALL-E 2 Edit API (DALL-E 3 no soporta edits aún)
        # Por ahora, regenerar con prompt modificado
        return {
            'success': False,
            'error': 'Edit functionality not yet implemented. Use generate with new prompt instead.'
        }


class MockDesignGenerator(DesignGenerator):
    """Versión de prueba que simula generación de diseños"""

    def __init__(self):
        pass

    def generate_social_post_design(self, design_spec: Dict) -> Dict:
        print(f"[MOCK] Generando diseño:")
        print(f"  Concepto: {design_spec.get('concept', 'N/A')}")
        print(f"  Colores: {design_spec.get('colors', [])}")
        print(f"  Estilo: {design_spec.get('style', 'N/A')}")

        # Simular guardado local
        today = datetime.now().strftime('%Y-%m-%d')
        mock_path = f'/Users/hernanazocar/developers/agentes-org/assets/marketing/{today}/mock_{design_spec.get("post_id", "design")}.png'

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(mock_path), exist_ok=True)

        # Crear archivo placeholder
        with open(mock_path, 'w') as f:
            f.write('MOCK IMAGE PLACEHOLDER')

        return {
            'success': True,
            'image_url': 'https://placeholder.com/mock-design.png',
            'local_path': mock_path,
            'prompt_used': 'MOCK PROMPT',
            'model': 'mock-dall-e-3',
            'mode': 'mock'
        }

    def generate_variations(self, image_url: str, n: int = 2) -> Dict:
        return {
            'success': True,
            'variations': [f'https://placeholder.com/variation-{i}.png' for i in range(n)],
            'count': n,
            'mode': 'mock'
        }
