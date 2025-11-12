
import os
import re
import time
import click
import functools
import __main__

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

    @click.group(invoke_without_command=True)
    @click.pass_context
    def group(ctx: click.Context):
        if ctx.invoked_subcommand is None:
            for name in group.list_commands(ctx):
                cmd = group.get_command(ctx, name)
                ctx.invoke(cmd)

    for part, func in parts:
        group.add_command(make_part_command(quest, part, func))
    return group

def make_part_command(quest, part, func):
    @click.command()
    @click.option('--notes', 'notes_file', type=click.File('r'))
    @click.pass_context
    @functools.wraps(func)
    def command(ctx, notes_file, **params):
        if notes_file is None:
            notes = get_notes(quest, part, ctx)
        else:
            notes = notes_file.read()
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

def get_notes(quest, part, ctx):
    path = f'notes/everybody_codes_e{event}_q{quest:02d}_p{part}.txt'
    if not os.path.exists(path):
        ctx.fail(f'Missing notes file: {path}')
    with open(path, 'r') as file:
        return file.read()

def timed(func):
    @functools.wraps(func)
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
