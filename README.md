# Hugging Face Upload Node for ComfyUI

This is a custom node for ComfyUI that allows you to upload models (checkpoints or Diffusers models) directly to the Hugging Face Hub from your ComfyUI workflows.

## Features

*   Uploads models to the Hugging Face Hub.
*   Supports both checkpoint (`.ckpt`) and Diffusers model formats.
*   Automatically creates a repository on the Hub if it doesn't exist.
*   Optionally creates a model card with a preview image.
*   Handles cases where no `model_path` is provided by using the ComfyUI output directory.

## Installation

1. **Clone this repository into your `ComfyUI/custom_nodes` directory:**

    ```bash
    cd ComfyUI/custom_nodes
    git clone https://github.com/Ktiseos-Nyx/HFBackup_ComfyUINode
    ```

2. **Install the required Python packages:**

    This node requires the `huggingface_hub` and `Pillow` libraries. You need to install them manually in ComfyUI's Python environment.

    **Steps:**

    *   **Find ComfyUI's Python Environment:** The environment is usually located in `ComfyUI/venv` or `ComfyUI/python_embeded` (especially on Windows).
    *   **Activate the Environment:**
        *   **Windows:**
            ```bash
            ComfyUI\venv\Scripts\activate  
            # OR (if the above doesn't work)
            ComfyUI\python_embeded\python.exe -m venv .venv
            .\venv\Scripts\activate
            ```
        *   **macOS/Linux:**
            ```bash
            source ComfyUI/venv/bin/activate
            ```
    *   **Install Dependencies:**
        ```bash
        pip install huggingface_hub Pillow
        ```

3. **Restart ComfyUI:** Restart your ComfyUI instance so that it can load the new custom node and the installed dependencies.

## Usage

1. **Add the Node:** In the ComfyUI interface, add the "Hugging Face Upload" node to your workflow. You'll find it in the "utils" category.

2. **Connect Inputs:**
    *   **`hf_token`:** (Required) Your Hugging Face Hub write access token. Get it from your [Hugging Face profile settings](https://huggingface.co/settings/tokens).
    *   **`repo_id`:** (Required) The ID of your Hugging Face repository (e.g., `your_username/your_repo_name`).
    *   **`model_path`:** (Optional) The path to the model file or directory. If left empty, it defaults to the ComfyUI output directory.
    *   **`path_in_repo`:** (Optional) The path within the repository to store the model.
    *   **`model_type`:** Select either `ckpt` or `diffusers`.
    *   **`commit_message`:** A message for the commit.
    *   **`create_model_card`:** Check to create a model card.
    *   **`images`:** (Optional) Connect an `IMAGE` tensor (e.g., from a `Preview Image` node) to include a preview in the model card.

3. **Run the Workflow:** Execute your workflow. The node will upload the model to your specified Hugging Face Hub repository.

## Troubleshooting

*   If you encounter errors, check the ComfyUI console for messages.
*   Make sure you have activated the correct Python environment before installing dependencies.
*   Ensure that your Hugging Face token has write access to the specified repository.

## Notes

*   Uploading large models may take time. There is no progress bar in the ComfyUI interface.
*   This README assumes you are familiar with basic ComfyUI concepts and have a Hugging Face Hub account.

## License

see the LICENSE file for details. 
