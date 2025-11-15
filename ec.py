
import os
import re
import time
import click
import requests
import __main__
from functools import wraps
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import tempfile
import json

event = 2025

def part(n):
    def decorator(func):
        func.__part__ = n
        return func
    return decorator

def main():
    cli = make_quest_group(__main__)
    cli.main()

def make_quest_group(mod):
    quest = get_quest(mod)
    if quest is None:
        raise ValueError(f'Could not determine quest number for module: {mod}')

    parts = get_parts(mod)
    if len(parts) == 0:
        raise ValueError(f'No parts found in module: {mod}')

    group = click.Group()
    for part, func in parts:
        group.add_command(make_part_command(quest, part, func))
    return group

def make_part_command(quest, part, func):
    @click.command()
    @click.option('--notes', 'notes_path', type=click.Path(exists=True))
    @click.option('--session', envvar='EC_SESSION')
    @wraps(func)
    def command(notes_path, session, **params):
        if notes_path is not None:
            with open(notes_path, 'r') as file:
                notes = file.read()
        else:
            notes = get_notes(quest, part, session)
        answer, answer_time = timed(func)(notes, **params)
        click.echo(f'{part}. {answer} [{format_time(answer_time)}]')
    return command

def get_quest(mod):
    try:
        return mod.__quest__
    except AttributeError:
        name, _ = os.path.splitext(os.path.basename(mod.__file__))
        if m := re.fullmatch(r'q(\d+)', name):
            return int(m.group(1))
        return None

def get_parts(mod):
    parts = []
    for attr in dir(mod):
        val = getattr(mod, attr)
        if callable(val) and (part := get_part(val)):
            parts.append((part, val))
    return parts

def get_part(func):
    try:
        return func.__part__
    except AttributeError:
        if m := re.fullmatch(r'p(\d+)', func.__name__):
            return int(m.group(1))
        return None

def timed(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return result, end_time - start_time
    return new_func

def format_time(time):
    for unit in ['s', 'ms', 'µs']:
        if time >= 1:
            return f"{time:.2f} {unit}"
        time *= 1000
    return f"{time:.2f} ns"

def get_notes(quest, part, session):
    notes_path = f'notes/everybody_codes_e{event}_q{quest:02d}_p{part}.txt'
    if os.path.exists(notes_path):
        with open(notes_path, 'r') as file:
            return file.read()
    else:
        notes = fetch_notes(quest, part, session)
        with open(notes_path, 'w') as file:
            file.write(notes)
        return notes

def fetch_notes(quest, part, session):
    if session is None:
        raise click.UsageError('A session is required to download notes automatically.')

    user = api('user/me', session)
    name = user.get('name')
    seed = user.get('seed', 0)
    if name is None:
        raise click.UsageError('No user logged in.')

    data = api(f'event/{event}/quest/{quest}', session)
    key = data.get(f'key{part}')
    if key is None:
        raise click.UsageError(f'Part {part} locked for user {name}.')

    encrypted_notes = assets(f'{event}/{quest}/input/{seed}.json')
    return decrypt(encrypted_notes[str(part)], key)

def api(path, session):
    res = requests.get('https://everybody.codes/api/' + path, cookies={ 'everybody-codes': session })
    res.raise_for_status()
    return res.json()

def assets(path):
    cache_file = os.path.join(tempfile.gettempdir(), 'everybody-codes', 'assets', *path.split('/'))
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            return json.load(file)

    res = requests.get('https://everybody-codes.b-cdn.net/assets/' + path)
    res.raise_for_status()
    data = res.json()

    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, 'w') as file:
        json.dump(data, file)

    return data

def decrypt(encrypted, key):
    iv = key[:16].encode('utf-8')
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    padded = cipher.decrypt(bytes.fromhex(encrypted))
    return unpad(padded, AES.block_size).decode('utf-8')
