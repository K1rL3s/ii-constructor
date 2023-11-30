from .projects import *
from .states import State

FILENAME = 'testProject'

def test_newProject():
    ''' Создание проекта '''
    
    input: Project.StartProjectData = Project.StartProjectData()
    input.name = 'Test123'
    input.db_name = 'Test123'
    input.file_path = 'Test123'
    input.hello = 'Test123'
    input.help = 'Test123'
    input.info = 'Test123'

    new_project: Project = ProjectsRepository.create(input)
    assert Project.data().name == input.name
    assert Project.data().db_name == input.db_name
    assert Project.data().file_path == input.file_path
    assert Project.data().hello.content == input.hello
    assert Project.data().help.content == input.help
    assert Project.data().info.content == input.info