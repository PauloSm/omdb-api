from google.auth import default


def get_project_id():
    _, project_id = default()
    return project_id
