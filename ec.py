
import os
import re
import time
import click
import inspect
import functools
import __main__

event = 2025
default_notes_path = 'notes/everybody_codes_e{}_q{:02d}_p{}.txt'

def main():
    cli = make_quest_group(__main__)
    cli.main()

def make_quest_group(mod):
    quest = detect_quest(mod)
    parts = detect_parts(mod)

    @click.group(invoke_without_command=True)
    @click.pass_context
    def group(ctx: click.Context):
        if ctx.invoked_subcommand is None:
            for part, func in parts:
                with open(default_notes_path.format(event, quest, part)) as file:
                    click.echo(str(func(file.read())))

    for part, func in parts:
        group.add_command(make_part_command(quest, part, func))
    return group

def make_part_command(quest, part, func):
    @click.command()
    @click.option('--notes', type=click.File('r'), default=default_notes_path.format(event, quest, part))
    @functools.wraps(func)
    def new_func(notes, **params):
        answer, answer_time = timed(func)(notes.read(), **params)
        click.echo(f'Answer: {answer}')
        click.echo()
        click.echo(f'Took {format_time(answer_time)}')
    return new_func

def detect_quest(mod):
    name, _ = os.path.splitext(os.path.basename(inspect.getfile(mod)))
    m = re.match(r'q([0-9]{2})', name)
    if not m:
        raise ValueError(f"Could not determine quest number from filename: {mod.__file__}")
    return int(m.group(1))

def detect_parts(mod):
    parts = []
    for name, func in inspect.getmembers(mod, inspect.isfunction):
        if m := re.match(r'p([0-9]+)', name):
            parts.append((int(m.group(1)), func))
    return parts

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
