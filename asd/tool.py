
import sys
import inspect
import importlib
from abc import ABCMeta, abstractmethod
from .system_config import load_config, save_config

class ToolBase(object):
    __metaclass__ = ABCMeta

    name = None
    desc = None
    example_config = {}

    def __init__(self, config = {}):
        self.config = config

    @abstractmethod
    def register(self, parser):
        pass

    @abstractmethod
    def process(self, args):
        pass

class ToolHelper():

    @staticmethod
    def _get_tool_classes(name):
        external_module = importlib.import_module(name)
        for type_name, type in inspect.getmembers(external_module):
            if inspect.isclass(type) and type is not ToolBase and ToolBase in inspect.getmro(type):
                yield type

    @staticmethod
    def register_external_tools_module(name):
        config = load_config('/etc')
        if 'external_tools' not in config:
            config['external_tools'] = dict()
        config['external_tools'][name] = {}
        for type in ToolHelper._get_tool_classes(name):
            if type.name not in config['external_tools'][name]:
                config['external_tools'][name][type.name] = dict(
                    enabled = True,
                    config = type.example_config,
                )
        save_config(config)

    @staticmethod
    def load_external_tools(system_config, user_config):
        tools = []
        for name in system_config:
            for type in ToolHelper._get_tool_classes(name):
                try:
                    cfg = system_config[name][type.name]
                except KeyError as e:
                    import json
                    print("system_config: {}, name: {}, type.name: {}".format(json.dumps(system_config, indent = 2), name, type.name))
                    raise
                if name in user_config and type.name in user_config[name]:
                    cfg = user_config[name][type.name]
                if cfg['enabled']:
                    tools.append(type(cfg['config']))
        return tools
