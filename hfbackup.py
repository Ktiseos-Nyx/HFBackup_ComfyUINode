import os
import folder_paths
from huggingface_hub import HfApi, ModelCard, create_repo
from huggingface_hub.utils import validate_repo_id, HfHubHTTPError

class HuggingFaceUpload:
    def __init__(self):
        self.api = HfApi()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "hf_token": ("STRING", {"multiline": False, "default": ""}),
                "repo_id": ("STRING", {"multiline": False, "default": "your_username/repo_name"}),
                "model_path": ("STRING", {"multiline": False, "default": ""}),  # Now optional
                "path_in_repo": ("STRING", {"multiline": False, "default": ""}),
                "model_type": (["ckpt", "diffusers"],),
                "commit_message": ("STRING", {"multiline": False, "default": "Upload from ComfyUI"}),
                "create_model_card": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "images": ("IMAGE",), # Image input
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "upload_to_hf"
    CATEGORY = "utils"

    def upload_to_hf(self, hf_token, repo_id, model_path, path_in_repo, model_type, commit_message, create_model_card, images=None):
        if not hf_token:
            print("\033[91mHugging Face Hub token is empty. Aborting upload.\033[0m")  # Red error message
            return ()

        if not model_path:
            # Get the ComfyUI output directory
            output_dir = folder_paths.get_output_directory()
            print(f"\033[93mModel path is empty, defaulting to ComfyUI output directory: {output_dir}\033[0m")  # Yellow warning message
            model_path = output_dir

        # Check if repo_id is valid
        try:
            validate_repo_id(repo_id)
        except ValueError as e:
            print(f"\033[91mInvalid repo_id: {e}\033[0m")  # Red error message
            return ()

        # Create repo if it doesn't exist
        try:
            repo_url = self.api.create_repo(token=hf_token, repo_id=repo_id, exist_ok=True)
            print(f"\033[92mRepo '{repo_id}' created or already exists: {repo_url}\033[0m")  # Green success message
        except HfHubHTTPError as e:
            print(f"\033[91mError creating repo: {e}\033[0m")
            return ()

        # Upload the model
        try:
            if model_type == "diffusers":
                print(f"\033[94mUploading diffusers model from '{model_path}' to '{repo_id}'\033[0m")  # Blue info message
                upload_url = self.api.upload_folder(
                    repo_id=repo_id,
                    folder_path=model_path,
                    path_in_repo=path_in_repo,
                    commit_message=commit_message,
                    token=hf_token
                )
            else:  # ckpt
                print(f"\033[94mUploading checkpoint from '{model_path}' to '{repo_id}'\033[0m")  # Blue info message
                # If it's a directory, upload the whole directory as a ckpt
                if os.path.isdir(model_path):
                    upload_url = self.api.upload_folder(
                        repo_id=repo_id,
                        folder_path=model_path,
                        path_in_repo=path_in_repo,
                        commit_message=commit_message,
                        token=hf_token
                    )
                else:
                    # Assume it's a single file if not a directory
                    upload_url = self.api.upload_file(
                        repo_id=repo_id,
                        path_or_fileobj=model_path,
                        path_in_repo=os.path.join(path_in_repo, os.path.basename(model_path)),
                        commit_message=commit_message,
                        token=hf_token
                    )

            print(f"\033[92mModel uploaded to: {upload_url}\033[0m")  # Green success message
        except Exception as e:
            print(f"\033[91mError uploading model: {e}\033[0m")
            return ()

        # Create a model card (optional)
        if create_model_card:
            try:
                if images is not None:
                    # Save the preview image to a temporary file
                    from PIL import Image
                    import numpy as np
                    import tempfile

                    # Convert the tensor to a PIL Image
                    i = 255. * images[0].cpu().numpy()
                    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                        img.save(tmp_file, format="PNG")
                        preview_image_path = tmp_file.name

                    card = ModelCard.from_template(
                        card_data={},  # You can add more metadata here
                        template_path=None,
                        model_id=repo_id,
                        license="mit",  # Change the license if needed
                        library_name="diffusers" if model_type == "diffusers" else "stable-diffusion",  # Or other appropriate library
                        tags=["stable-diffusion", "comfyui"],  # Add relevant tags
                        image_path=preview_image_path
                    )

                    # Remove the temporary image file
                    os.remove(preview_image_path)
                else:
                    card = ModelCard.from_template(
                        card_data={},
                        template_path=None,
                        model_id=repo_id,
                        license="mit",
                        library_name="diffusers" if model_type == "diffusers" else "stable-diffusion",
                        tags=["stable-diffusion", "comfyui"],
                    )

                card.push_to_hub(repo_id, token=hf_token)
                print(f"\033[92mModel card created in '{repo_id}'\033[0m")
            except Exception as e:
                print(f"\033[91mError creating model card: {e}\033[0m")

        return ()

# Register the node
NODE_CLASS_MAPPINGS = {
    "HuggingFaceUpload": HuggingFaceUpload
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HuggingFaceUpload": "Hugging Face Upload"
}
