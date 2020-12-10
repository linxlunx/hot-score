from app import manager
from command.user import create_superuser
from command.dataset import import_base_images


@manager.command
def add_superuser():
    """Create New Admin User"""
    create_superuser()


@manager.command
def import_images():
    """Import Base Images"""
    import_base_images()


if __name__ == '__main__':
    manager.run()
