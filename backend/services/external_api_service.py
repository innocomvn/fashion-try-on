"""
PHƯƠNG ÁN 2: External API Virtual Try-On Service
Sử dụng các API service bên ngoài: Replicate, Fal.ai, HeyBeauty
"""

import time
import requests
import json
from typing import Dict, Optional
from urllib.request import urlretrieve
import replicate
import os

from backend.config import settings


class ExternalAPIVirtualTryOn:
    """
    External API virtual try-on service
    Supports: Replicate, Fal.ai, HeyBeauty
    """

    def __init__(self, provider: str = None):
        self.provider = provider or settings.API_PROVIDER
        print(f"Initializing {self.provider} API service...")

    def process_tryon(
        self,
        model_image_path: str,
        garment_image_path: str,
        output_path: str,
        category: str = "upperbody",
        denoise_steps: int = 30,
        **kwargs
    ) -> Dict:
        """
        Process virtual try-on using external API

        Args:
            model_image_path: Path to model/person image
            garment_image_path: Path to garment image
            output_path: Path to save result
            category: Garment category
            denoise_steps: Number of denoising steps

        Returns:
            Dict with result information
        """
        start_time = time.time()

        try:
            if self.provider == "replicate":
                result = self._process_replicate(
                    model_image_path, garment_image_path, output_path,
                    category, denoise_steps
                )
            elif self.provider == "fal":
                result = self._process_fal(
                    model_image_path, garment_image_path, output_path,
                    category, denoise_steps
                )
            elif self.provider == "heybeauty":
                result = self._process_heybeauty(
                    model_image_path, garment_image_path, output_path,
                    category, denoise_steps
                )
            else:
                raise ValueError(f"Unknown provider: {self.provider}")

            processing_time = time.time() - start_time
            result['processing_time'] = processing_time

            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }

    def _process_replicate(
        self,
        model_image_path: str,
        garment_image_path: str,
        output_path: str,
        category: str,
        denoise_steps: int
    ) -> Dict:
        """
        Process using Replicate API
        Model: IDM-VTON on Replicate
        API Docs: https://replicate.com/cuuupid/idm-vton
        """

        if not settings.REPLICATE_API_TOKEN:
            return {
                'success': False,
                'error': 'Replicate API token not configured. Set REPLICATE_API_TOKEN in .env'
            }

        try:
            # Set API token
            os.environ['REPLICATE_API_TOKEN'] = settings.REPLICATE_API_TOKEN

            print(f"Calling Replicate API with model: {settings.REPLICATE_MODEL}")

            # Upload images and run prediction
            with open(model_image_path, 'rb') as model_file, \
                 open(garment_image_path, 'rb') as garment_file:

                output = replicate.run(
                    settings.REPLICATE_MODEL,
                    input={
                        "human_img": model_file,
                        "garm_img": garment_file,
                        "garment_des": category,
                        "seed": 42,
                        "n_steps": denoise_steps
                    }
                )

            # Download result
            if output:
                # output is usually a URL or FileOutput object
                result_url = str(output) if not isinstance(output, str) else output
                print(f"Downloading result from: {result_url}")
                urlretrieve(result_url, output_path)

                return {
                    'success': True,
                    'output_path': output_path,
                    'provider': 'replicate',
                    'result_url': result_url
                }
            else:
                return {
                    'success': False,
                    'error': 'No output received from Replicate'
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'Replicate API error: {str(e)}'
            }

    def _process_fal(
        self,
        model_image_path: str,
        garment_image_path: str,
        output_path: str,
        category: str,
        denoise_steps: int
    ) -> Dict:
        """
        Process using Fal.ai API
        Model: IDM-VTON on Fal.ai
        API Docs: https://fal.ai/models/idm-vton
        """

        if not settings.FAL_API_KEY:
            return {
                'success': False,
                'error': 'Fal.ai API key not configured. Set FAL_API_KEY in .env'
            }

        try:
            import fal_client

            print(f"Calling Fal.ai API with model: {settings.FAL_MODEL}")

            # Upload images to Fal.ai storage
            with open(model_image_path, 'rb') as f:
                model_url = fal_client.upload_file(f)

            with open(garment_image_path, 'rb') as f:
                garment_url = fal_client.upload_file(f)

            # Submit job
            handler = fal_client.submit(
                settings.FAL_MODEL,
                arguments={
                    "human_img_url": model_url,
                    "garment_img_url": garment_url,
                    "category": category,
                    "num_inference_steps": denoise_steps
                }
            )

            # Wait for result
            result = handler.get()

            # Download result
            if result and 'image' in result:
                result_url = result['image']['url']
                print(f"Downloading result from: {result_url}")
                urlretrieve(result_url, output_path)

                return {
                    'success': True,
                    'output_path': output_path,
                    'provider': 'fal',
                    'result_url': result_url
                }
            else:
                return {
                    'success': False,
                    'error': 'No output received from Fal.ai'
                }

        except ImportError:
            return {
                'success': False,
                'error': 'fal-client not installed. Run: pip install fal-client'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Fal.ai API error: {str(e)}'
            }

    def _process_heybeauty(
        self,
        model_image_path: str,
        garment_image_path: str,
        output_path: str,
        category: str,
        denoise_steps: int
    ) -> Dict:
        """
        Process using HeyBeauty API
        Uses the existing code from FastApis/fast01_influence.py
        API Docs: https://heybeauty.ai/keys
        """

        if not all([settings.HEYBEAUTY_API_URL, settings.HEYBEAUTY_OPEN_ID,
                    settings.HEYBEAUTY_API_KEY, settings.HEYBEAUTY_OSS_URL]):
            return {
                'success': False,
                'error': 'HeyBeauty API credentials not configured. Set HEYBEAUTY_* variables in .env'
            }

        try:
            api_url = settings.HEYBEAUTY_API_URL
            open_id = settings.HEYBEAUTY_OPEN_ID
            api_key = settings.HEYBEAUTY_API_KEY
            oss_url = settings.HEYBEAUTY_OSS_URL

            # Extract filenames
            pose_name = os.path.basename(model_image_path)
            cloth_name = os.path.basename(garment_image_path)

            # Step 1: Get upload URLs
            params = {
                'openId': open_id,
                'apiKey': api_key,
                'ipId': '',
                'poseFileName': pose_name,
                'maskFileName': '',
                'clothFileName': cloth_name
            }

            print("Step 1: Requesting upload URLs from HeyBeauty...")
            ret = requests.post(
                f"{api_url}/api/inf/fastinf_upload",
                data=json.dumps(params),
                timeout=settings.API_TIMEOUT
            )

            if ret.status_code != 200 or 'data' not in ret.json():
                return {
                    'success': False,
                    'error': f'Failed to get upload URLs: {ret.json()}'
                }

            data = ret.json()['data']
            inf_id = data['infId']
            cloth_url = data['clothUrl']
            pose_url = data['poseUrl']

            print(f"Got infId: {inf_id}")

            # Step 2: Upload images
            print("Step 2: Uploading images...")
            with open(garment_image_path, 'rb') as f:
                response = requests.put(cloth_url, data=f)
                if response.status_code != 200:
                    raise Exception('Failed to upload garment image')

            with open(model_image_path, 'rb') as f:
                response = requests.put(pose_url, data=f)
                if response.status_code != 200:
                    raise Exception('Failed to upload model image')

            # Step 3: Publish task
            print("Step 3: Publishing task...")
            params = {
                'openId': open_id,
                'apiKey': api_key,
                'infId': inf_id,
                'denoise_steps': denoise_steps,
                'auto_mask': 1,
                'auto_crop': 1,
                'category': 2,  # Map category to HeyBeauty format
                'caption': ""
            }

            ret = requests.post(
                f"{api_url}/api/inf/public_fastinf",
                data=json.dumps(params),
                timeout=settings.API_TIMEOUT
            )

            if ret.status_code != 200 or 'data' not in ret.json():
                return {
                    'success': False,
                    'error': f'Failed to publish task: {ret.json()}'
                }

            print("Task published successfully!")

            # Step 4: Poll for result
            print("Step 4: Waiting for result...")
            time.sleep(20)  # Initial wait

            for attempt in range(30):
                params = {'openId': open_id, 'apiKey': api_key, 'infId': inf_id}
                ret = requests.post(
                    f"{api_url}/api/inf/get_fast_result",
                    data=json.dumps(params),
                    timeout=settings.API_TIMEOUT
                )

                if ret.status_code == 200 and 'data' in ret.json():
                    data = ret.json()['data']
                    state = data['state']

                    if state == 2:  # Completed
                        result_url = oss_url + data['showUrl']
                        print(f"Task completed! Downloading from: {result_url}")
                        urlretrieve(result_url, output_path)

                        return {
                            'success': True,
                            'output_path': output_path,
                            'provider': 'heybeauty',
                            'result_url': result_url
                        }
                    elif state == -1:  # Failed
                        return {
                            'success': False,
                            'error': f"Task failed: {data.get('infInfoEn', 'Unknown error')}"
                        }
                    elif state == 1:  # In queue
                        position = data.get('position', 0)
                        print(f"Task in queue, position: {position}")

                time.sleep(5)

            return {
                'success': False,
                'error': 'Task timeout - took too long to complete'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'HeyBeauty API error: {str(e)}'
            }


def get_external_api_service(provider: str = None) -> ExternalAPIVirtualTryOn:
    """Get external API service instance"""
    return ExternalAPIVirtualTryOn(provider)
