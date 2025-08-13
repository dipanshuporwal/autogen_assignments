from jinja2 import Environment, FileSystemLoader
import os

# Set up the environment once
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
env = Environment(loader=FileSystemLoader(PROMPT_DIR))


def get_prompt_message_from_template(
    template_name: str, prompt_type: str, **kwargs
) -> str:
    """
    Renders a Jinja2 template from a specific subfolder ('sys_prompts' or 'user_prompts').

    Args:
        template_name (str): Name of the Jinja2 template file.
        prompt_type (str): Type of prompt - "sys" or "user". Defaults to "sys".
        **kwargs: Context variables to inject into the template.

    Returns:
        str: Rendered template content.
    """
    if prompt_type not in {"sys", "usr"}:
        raise ValueError("prompt_type must be either 'sys' or 'usr'")

    subfolder = "sys_prompts" if prompt_type == "sys" else "usr_prompts"
    full_template_path = os.path.join(subfolder, template_name)

    template = env.get_template(full_template_path)
    return template.render(**kwargs)
