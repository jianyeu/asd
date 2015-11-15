import sys
import json
import argparse

from .tool import ToolBase

class PathSearchException(Exception):
    pass

class InvalidListIndexException(PathSearchException):
    pass

class JSONBrowser(ToolBase):
    """
    Browse json encoded data by keys.
    """
    name = 'json'

    def register(self, parser):
        parser.add_argument('infile', nargs = '?', type = argparse.FileType('r'), default = sys.stdin)
        parser.add_argument('-p', '--path', default = '')
        parser.add_argument('-k', '--key_list', action = 'store_true')

    def get_sub_value(self, data, path_array):
        if len(path_array) == 0 or path_array[0] == '':
            return data
        key = path_array.pop(0)
        data_type = type(data)
        if data_type is list:
            if key.isdigit():
                key = int(key)
                if key < 0 or key >= len(data):
                    raise PathSearchException()
            elif key.find(':') != -1:
                sub_keys = key.split(':')
                start_key = sub_keys[0] if len(sub_keys[0]) else 0
                end_key = sub_keys[1] if len(sub_keys[1]) else len(data)
                try:
                    start_key = int(start_key)
                    end_key = int(end_key)
                except ValueError as e:
                    raise InvalidListIndexException()
                return data[start_key:end_key]
            else:
                raise PathSearchException()
        else:
            if key not in data:
                raise PathSearchException()
        return self.get_sub_value(data[key], path_array)

    def process(self, args):
        try:
            data = json.load(args.infile)
            sub_value = self.get_sub_value(data, args.path.split('.'))
            if type(sub_value) is dict or type(sub_value) is list:
                if args.key_list:
                    if type(sub_value) is dict:
                        print json.dumps(sub_value.keys(), indent = 4)
                    else:
                        print range(len(sub_value))
                else:
                    print json.dumps(sub_value, indent = 4)
            else:
                print sub_value

        except ValueError as e:
            print 'Could not decode json: %s' % e
        except InvalidListIndexException as e:
            print 'Invalid list index: "%s"' % args.path
        except PathSearchException as e:
            print 'Could not find the specified path: "%s"' % args.path


