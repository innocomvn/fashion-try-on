"""
Test script for Fashion Try-On API

Usage:
    python test_api.py --model person.jpg --garment shirt.jpg --provider replicate
"""

import argparse
import requests
import time
import os
from pathlib import Path


def test_tryon_api(
    model_image_path: str,
    garment_image_path: str,
    provider: str = "replicate",
    api_url: str = "http://localhost:8000"
):
    """
    Test the virtual try-on API

    Args:
        model_image_path: Path to model/person image
        garment_image_path: Path to garment image
        provider: Provider to use (on_premise, replicate, fal, heybeauty)
        api_url: API base URL
    """
    print("=" * 60)
    print("Fashion Try-On API Test")
    print("=" * 60)

    # Check if files exist
    if not os.path.exists(model_image_path):
        print(f"❌ Error: Model image not found: {model_image_path}")
        return

    if not os.path.exists(garment_image_path):
        print(f"❌ Error: Garment image not found: {garment_image_path}")
        return

    print(f"\n📸 Model image: {model_image_path}")
    print(f"👔 Garment image: {garment_image_path}")
    print(f"🔧 Provider: {provider}")
    print(f"🌐 API URL: {api_url}")

    # Step 1: Health check
    print("\n[1/4] Checking API health...")
    try:
        response = requests.get(f"{api_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy!")
            print(f"   Version: {data['version']}")
            print(f"   On-premise available: {data['on_premise_available']}")
            print(f"   External API available: {data['external_api_available']}")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return

    # Step 2: Create try-on task
    print("\n[2/4] Creating try-on task...")
    try:
        with open(model_image_path, 'rb') as model_file, \
             open(garment_image_path, 'rb') as garment_file:

            files = {
                'model_image': model_file,
                'garment_image': garment_file
            }
            data = {
                'provider': provider,
                'category': 'upperbody',
                'denoise_steps': 30,
                'seed': 42
            }

            response = requests.post(
                f"{api_url}/api/v1/tryon",
                files=files,
                data=data
            )

            if response.status_code == 200:
                result = response.json()
                task_id = result['task_id']
                print(f"✅ Task created successfully!")
                print(f"   Task ID: {task_id}")
                print(f"   Status: {result['status']}")
                print(f"   Message: {result['message']}")
            else:
                print(f"❌ Failed to create task: {response.status_code}")
                print(f"   Error: {response.text}")
                return

    except Exception as e:
        print(f"❌ Error creating task: {e}")
        return

    # Step 3: Poll for task completion
    print(f"\n[3/4] Waiting for task to complete...")
    print("   (This may take 20-60 seconds depending on the provider)")

    max_attempts = 60
    attempt = 0

    while attempt < max_attempts:
        try:
            response = requests.get(f"{api_url}/api/v1/tryon/{task_id}")

            if response.status_code == 200:
                status_data = response.json()
                status = status_data['status']
                progress = status_data['progress']

                print(f"   Progress: {progress}% - Status: {status}", end='\r')

                if status == 'completed':
                    print(f"\n✅ Task completed!")
                    print(f"   Processing time: {status_data.get('processing_time', 'N/A')} seconds")
                    print(f"   Result URL: {api_url}{status_data['result_url']}")
                    break
                elif status == 'failed':
                    print(f"\n❌ Task failed!")
                    print(f"   Error: {status_data.get('error_message', 'Unknown error')}")
                    return

            time.sleep(2)
            attempt += 1

        except Exception as e:
            print(f"\n❌ Error checking status: {e}")
            return

    if attempt >= max_attempts:
        print(f"\n⏱️  Timeout: Task took too long to complete")
        return

    # Step 4: Download result
    print(f"\n[4/4] Downloading result...")
    try:
        response = requests.get(f"{api_url}/api/v1/tryon/{task_id}/result")

        if response.status_code == 200:
            output_filename = f"result_{task_id}.jpg"
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Result saved to: {output_filename}")
        else:
            print(f"❌ Failed to download result: {response.status_code}")
            return

    except Exception as e:
        print(f"❌ Error downloading result: {e}")
        return

    print("\n" + "=" * 60)
    print("✨ Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Fashion Try-On API")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to model/person image"
    )
    parser.add_argument(
        "--garment",
        type=str,
        required=True,
        help="Path to garment/clothing image"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="replicate",
        choices=["on_premise", "replicate", "fal", "heybeauty"],
        help="Provider to use"
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default="http://localhost:8000",
        help="API base URL"
    )

    args = parser.parse_args()

    test_tryon_api(
        model_image_path=args.model,
        garment_image_path=args.garment,
        provider=args.provider,
        api_url=args.api_url
    )
