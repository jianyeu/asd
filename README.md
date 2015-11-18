What is this?
=============
Place for various command line tools.

Why 'asd' ?
===========
Easy to type, because it's short and qwerty.

Install
=======
``pip install asd``

For bash completion activate argcomplete:

``activate-global-python-argcomplete``

If the global activation is not working or you just don't want to activate globally, completion could install locally by add this line the end of the ~/.bashrc file:

``eval "$(register-python-argcomplete asd)"``

Available tools
===============
- JSON browser: 
    - parse and display json data with human readable format
    - help: ``asd json -h``
    - usage: 
        - ``asd json path/to/data.json``
        - ``cat path/to/data.json | asd json``
        - ``asd json < path/to/data.json``
    - display sub-data only: ``asd json path/to/data.json -p path.to.sub.data``
    - **bash completion** is available for sub-data too (working only if the json file is parameter, not piped data)
