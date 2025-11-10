
import os
import re
import time
import click
import inspect
import functools
import __main__

event = 2025

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
            total_time = 0.0
            for part, func in parts:
                answer, answer_time = timed(func)(get_notes(quest, part, ctx))
                total_time += answer_time
                click.echo(f'- Part {part}: {answer}')
                click.echo(f'  Took {format_time(answer_time)}')
                click.echo()
            click.echo(f'Took in total {format_time(total_time)}')

    for part, func in parts:
        group.add_command(make_part_command(quest, part, func))
    return group

def make_part_command(quest, part, func):
    @click.command()
    @click.option('--notes', 'notes_file', type=click.File('r'))
    @click.pass_context
    @functools.wraps(func)
    def new_func(ctx, notes_file, **params):
        if notes_file is None:
            notes = get_notes(quest, part, ctx)
        else:
            notes = notes_file.read()
        answer, answer_time = timed(func)(notes, **params)
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

def get_notes(quest, part, ctx):
    path = f'notes/everybody_codes_e{event}_q{quest:02d}_p{part}.txt'
    if not os.path.exists(path):
        ctx.fail()
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
