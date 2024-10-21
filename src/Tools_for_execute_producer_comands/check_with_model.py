from src.Tools_for_compile_the_model.get_saved_model import classify


def get_result_from_HADES(message: str) -> bool:
    return classify([message])