from pathlib import Path
from uuid import UUID

def create_directory(directories: list[Path]):
    for directory in directories:
        if not directory.exists():
            directory.mkdir()


def get_project_directory_path(directory_name: UUID) -> Path:
    directory_path = Path(PROJECTS_DIRECTORY_PATH / f'{directory_name}')
    create_directory([directory_path])
    
    return directory_path


ROOT_PATH = Path(__file__).resolve().parent.parent.parent
SRC_DIRECTORY_PATH = Path(ROOT_PATH / 'src')

ENVIRONMENTS_DIRECTORY_PATH = Path(SRC_DIRECTORY_PATH / 'environments')
ENVIRONMENT_FILE_NAME = 'settings.env'
ENVIRONMENT_FILE_PATH = Path(ENVIRONMENTS_DIRECTORY_PATH / ENVIRONMENT_FILE_NAME)
STATIC_DIRECTORY_PATH = Path(SRC_DIRECTORY_PATH / 'static')
STORAGE_DIRECTORY_PATH = Path(STATIC_DIRECTORY_PATH / 'storage')
LOG_DIRECTORY_PATH = Path(STATIC_DIRECTORY_PATH / 'logs')
UPLOADS_DIRECTORY_PATH = Path(STATIC_DIRECTORY_PATH / 'uploads')

PROJECTS_DIRECTORY_PATH = Path(STATIC_DIRECTORY_PATH / 'projects')


create_directory(
    [
        STATIC_DIRECTORY_PATH,
        LOG_DIRECTORY_PATH,
        
        PROJECTS_DIRECTORY_PATH,
        STORAGE_DIRECTORY_PATH,
    ]
)

LOG_FILE_NAME = 'events.log'
LOG_FILE_PATH = Path(LOG_DIRECTORY_PATH / LOG_FILE_NAME)
