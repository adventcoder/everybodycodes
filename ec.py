
import os
import re
import time
import click
import requests
import __main__
from functools import wraps
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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
    @pass_notes(quest, part)
    @wraps(func)
    def command(notes, **params):
        answer, answer_time = timed(func)(notes, **params)
        click.echo(f'{part}. {answer} [{format_time(answer_time)}]')
    return command

def pass_notes(quest, part):
    def decorator(func):
        @click.option('--notes', 'notes_path', type=click.Path(exists=True))
        @click.option('--session', envvar='EC_SESSION')
        @click.pass_context
        @wraps(func)
        def new_func(ctx: click.Context, notes_path, session, **params):
            if notes_path is not None:
                with open(notes_path, 'r') as file:
                    notes = file.read()
            else:
                notes_path = f'notes/everybody_codes_e{event}_q{quest:02d}_p{part}.txt'
                if os.path.exists(notes_path):
                    with open(notes_path, 'r') as file:
                        notes = file.read()
                else:
                    if session is None:
                        ctx.fail('A session is required to download notes automatically.')
                    notes = fetch_notes(quest, part, session)
                    with open(notes_path, 'w') as file:
                        file.write(notes)
            return func(notes, **params)
        return new_func
    return decorator

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

def fetch_notes(quest, part, session):
    with Client(session) as client:
        me = client.get_me()
        notes = client.get_notes(quest, me['seed'])
        quest = client.get_quest(quest)
        return decrypt(notes[f'{part}'], quest[f'key{part}'])

class Client:
    def __init__(self, session):
        self.session = requests.Session()
        self.session.cookies.set('everybody-codes', session, domain='everybody.codes')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.close()

    def get_me(self):
        res = self.session.get('https://everybody.codes/api/user/me')
        res.raise_for_status()
        return res.json()

    def get_quest(self, quest):
        res = self.session.get(f'https://everybody.codes/api/event/{event}/quest/{quest}')
        res.raise_for_status()
        return res.json()

    def get_notes(self, quest, seed):
        res = self.session.get(f'https://everybody-codes.b-cdn.net/assets/{event}/{quest}/input/{seed}.json')
        res.raise_for_status()
        return res.json()

def decrypt(encrypted, key):
    iv = key[:16].encode('utf-8')
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    padded = cipher.decrypt(bytes.fromhex(encrypted))
    return unpad(padded, AES.block_size).decode('utf-8')
