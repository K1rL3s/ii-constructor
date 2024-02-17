from alicetool.editor.domain.core import *

class StateMachineInterface(StateInterface, SynonymsInterface, FlowInterface):
    pass

class StateMachine(StateMachineInterface):
    def __init__(self):
        self.__states: StateFactory = StateFactory()
        self.__synonyms: SynonymsFactory = SynonymsFactory()
        self.__content: FlowFactory = FlowFactory()

    def get_state(self, id) -> State:
        return self.__states.state_obj(id)
    
    def get_synonyms(self, id) -> Synonyms:
        return self.__synonyms.synonyms_obj(id)
    
    def get_flow(self, id) -> Flow:
        return self.__content.flow_obj(id)
    
    def states_interface(self) -> StateInterface:
        return self.__states

    def synonyms_interface(self) -> SynonymsInterface:
        return self.__synonyms

    def content_interface(self) -> FlowInterface:
        return self.__content
    
    # states
    def create_state(self, data) -> int:
        return self.__states.create_state(data)
    
    def read_state(self, id: int) -> str:
        return self.__states.read_state(id)

    def update_state(self, id: int, new_data):
        return self.__states.update_state(id, new_data)

    def delete_state(self, id: int):
        return self.__states.delete_state(id)

    def states(self) -> set[int]:
        return self.__states.states()

    def set_state_notifier(self, notifier: StateActionsNotifier):
        return self.__states.set_state_notifier(notifier)

    # synonyms
    def create_synonyms(self, data) -> int:
        return self.__synonyms.create_synonyms(data)
    
    def read_synonyms(self, id: int) -> str:
        return self.__synonyms.create_synonyms(id)

    def update_synonyms(self, id: int, new_data):
        return self.__synonyms.create_synonyms(id, new_data)

    def delete_synonyms(self, id: int):
        return self.__synonyms.create_synonyms(id)

    def synonyms(self) -> set[int]:
        return self.__synonyms.create_synonyms()

    def set_synonyms_notifier(self, notifier: SynonymsActionsNotifier):
        return self.__synonyms.create_synonyms(notifier)

    # flows
    def create_flow(self, data, cmd) -> int:
        return self.__content.create_flow(data, cmd)
    
    def read_flow(self, id: int) -> str:
        return self.__content.read_flow(id)

    def update_flow(self, id: int, new_data):
        return self.__content.update_flow(id, new_data)

    def delete_flow(self, id: int):
        return self.__content.delete_flow(id)

    def flows(self) -> set[int]:
        return self.__content.flows()

    def set_flow_notifier(self, notifier: FlowActionsNotifier):
        return self.__content.set_flow_notifier(notifier)


class StateMachineNotifier(StateActionsNotifier, SynonymsActionsNotifier, FlowActionsNotifier):
    pass

class Project:
    __name: str = 'scenario name'
    __db_name: str = 'db_name'
    __file_path: str = 'path.proj'
    __content: StateMachine = None
    __entry_point: State = None
    __notifier: StateMachineNotifier = None
    
    def __str__(self):
        return '; '.join([
            f'id={self.__id}',
            f'name={self.__name}',
            f'db_name={self.__db_name}',
            f'file_path={self.__file_path}',
        ])

    @staticmethod
    def parse(data:str):
        _data = {}

        if data == '':
            return _data

        for item in data.split('; '):
            _item = item.split('=')

            if len(_item) != 2:
                raise AttributeError(
                    f'Плохие данные: синтаксическая ошибка "{item}"'
                )
            
            key = _item[0]
            value = _item[1]

            # if key not in ['id', 'name', 'db_name', 'file_path']:
            #     raise AttributeError(
            #         f'Плохие данные: неизвестный ключ "{key}"'
            #     )

            if key == 'id':
                _data[key] = int(value)

            else:
                quoted = len(value) > 2 and value[0] == '"' and value[-1] == '"'
                val = value[1:-1] if quoted else value
                _data[key] = val

        return _data

    def __init__(self, id:int, **kwargs):
        self.__content = StateMachine()

        if type(id) is not int:
            raise TypeError('первый позиционный аргумент "id" должен быть целым числом')
        
        self.__id: int = id

        arg_names = kwargs.keys()

        if 'name' in arg_names:
            quoted = len(kwargs['name']) > 2 and kwargs['name'][0] == '"' and kwargs['name'][-1] == '"'
            value = kwargs['name'][1:-1] if quoted else kwargs['name']
            self.__name = value
        
        if 'db_name' in arg_names:
            quoted = len(kwargs['db_name']) > 2 and kwargs['db_name'][0] == '"' and kwargs['db_name'][-1] == '"'
            value = kwargs['db_name'][1:-1] if quoted else kwargs['db_name']
            self.__db_name = value

        if 'file_path' in arg_names:
            quoted = len(kwargs['file_path']) > 2 and kwargs['file_path'][0] == '"' and kwargs['file_path'][-1] == '"'
            value = kwargs['file_path'][1:-1] if quoted else kwargs['file_path']
            self.__file_path = value

        hello_msg = ''
        if 'hello' in arg_names:
            quoted = len(kwargs['hello']) > 2 and kwargs['hello'][0] == '"' and kwargs['hello'][-1] == '"'
            hello_msg = kwargs['hello'][1:-1] if quoted else kwargs['hello']
            if len(hello_msg) > 1024:
                hello_msg = hello_msg[:1024]

        self.__entry_point = self.__content.get_state(
            self.__content.states_interface().create_state(
                f'name=Enter; content="{hello_msg}"'
            )
        )

    def id(self):
        return self.__id

    def name(self) -> str:
        return self.__name

    def db_name(self) -> str:
        return self.__db_name

    def file_path(self) -> str:
        return self.__file_path

    def content_interface(self) -> StateMachineInterface:
        return self.__content
    
    def set_notifier(self, notifier: StateMachineNotifier):
        if not issubclass(type(notifier), StateMachineNotifier):
            raise ValueError('notifier должен быть наследником класса StateMachineNotifier')
        
        self.__notifier = notifier

class ProjectsActionsNotifier:
    def created(self, id:int, data):
        raise NotImplementedError()

    def saved(self, id:int, data):
        raise NotImplementedError()

    def updated(self, id:int, new_data):
        raise NotImplementedError()

    def removed(self, id:int):
        raise NotImplementedError()

class ProjectsInterface:
    def create(self, data) -> int:
        raise NotImplementedError()
    
    def read(self, id: int):
        raise NotImplementedError()
    
    def read(self, db_name: str):
        raise NotImplementedError()
    
    def update(self, id: int, data):
        raise NotImplementedError()
    
    def delete(self, id: int):
        raise NotImplementedError()
    
    def open_file(self, path: str):
        raise NotImplementedError()
    
    def save_file(self, id: int):
        raise NotImplementedError()
    
    def publish(self, id: int):
        raise NotImplementedError()
    
    def set_notifier(self, notifier: ProjectsActionsNotifier):
        raise NotImplementedError()
    
    def set_content_notifier(self, 
        project_id: int, notifier: StateMachineNotifier
    ):
        raise NotImplementedError()

class ProjectsManager(ProjectsInterface):
    __items: dict[int, Project] = {}
    __notifier: ProjectsActionsNotifier = None

    def project(self, id: int) -> Project:
        if id not in self.__items.keys():
            raise ValueError(f'Проект с id={id} не существует')
        
        return self.__items[id]

    def __new__(cls):
        if not hasattr(cls, '_ProjectsManager__instance'):
            cls.__instance = super(ProjectsManager, cls).__new__(cls)
        
        return cls.__instance
    
    @staticmethod
    def instance() -> ProjectsInterface:
        return ProjectsManager()
    
    def create(self, data) -> int:
        id = 1
        
        current_len = len(self.__items)
        if current_len > 0:
            current_keys = list(self.__items.keys())
            last_key = current_keys[-1]

            # проверяем пропуски в id
            if current_len - last_key == 0:
                id = last_key + 1
            else:
                id = (set(range(1, last_key+1)) - set(current_keys) ).pop()

        _data: dict = Project.parse(data)

        new_proj = Project(id, **_data)

        new_proj_content: StateMachine = new_proj.content_interface()

# создаём обязательные флоу
        # Помощь
        msg = _data['help'] if 'help' in _data else ''
        state: State = new_proj_content.get_state(
            new_proj_content.create_state(
                f'name=Help; content={msg[:1024] if len(msg) > 1024 else msg}'
            )
        )
        cmds = ','.join(
            [
                '"Помощь"',
                '"Помоги"',
                '"Справка"',
            ]
        )
        synon: Synonyms = new_proj_content.get_synonyms(
            new_proj_content.create_synonyms(
                f'name=Help; values={cmds}'
            )
        )
        new_proj_content.create_flow(
            f'required=true; name=Help; '
            f'description="Помощь, например в навигации"',
            Command(state, synon)
        )

        # Что ты умеешь?
        msg = _data['info'] if 'info' in _data else ''
        state = new_proj_content.get_state(
            new_proj_content.create_state(
                f'name=Info; content={msg[:1024] if len(msg) > 1024 else msg}'
            )
        )
        cmds = ','.join(
            [
                '"Информация"',
                '"Что ты умеешь"',
            ]
        )
        synon = new_proj_content.get_synonyms(
            new_proj_content.create_synonyms(
                f'name=Info; values={cmds}'
            )
        )
        new_proj_content.create_flow(
            f'required=true; name=Info; '
            f'description="Информация, например описание команд"',
            Command(state, synon)
        )

        self.__items[id] = new_proj
        if self.__notifier is not None:
            self.__notifier.created(id, new_proj.__str__())
        
        return id
    
    def read(self, id: int):
        if id not in self.__items.keys():
            raise ValueError(f'Проект с id={id} не существует')

        return self.__items[id].__str__()
    
    # def read(self, db_name: str):
    #     pass
    
    # def update(self, id: int, data):
    #     pass
    
    def delete(self, id: int):
        if id not in self.__items.keys():
            raise ValueError(f'Проект с id={id} не существует')
        
        del self.__items[id]

        if self.__notifier is not None:
            self.__notifier.removed(id)
    
    # def open_file(self, path: str):
    #     pass
    
    # def save_file(self, id: int):
    #     pass
    
    # def publish(self, id: int):
    #     pass
    
    def set_notifier(self, notifier: ProjectsActionsNotifier):
        if not issubclass(type(notifier), ProjectsActionsNotifier):
            raise ValueError('notifier должен быть наследником класса ProjectsActionsNotifier')
        
        self.__notifier = notifier

    def set_content_notifier(self, 
        project_id: int, notifier: StateMachineNotifier
    ):  
        self.project(project_id).set_notifier(notifier)