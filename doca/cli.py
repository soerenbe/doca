import pathlib
import click
import logging
import os
import sys

from thefuzz import process
from pathlib import Path

_DEFAULT_DOCA_PATH = str(Path.home())

SEARCH_PATH = [Path(i) for i in os.environ.get('DOCA_PATH', _DEFAULT_DOCA_PATH).split(':')]
EXCLUDE_PATH = [Path(i) for i in os.environ.get('DOCA_EXCLUDE_PATH', '').split(':') if i]
EDITOR = os.environ.get('EDITOR', 'nano')

logging.basicConfig(
    level=os.environ.get('DOCA_LOGLEVEL', 'warning').upper(),
    format="%(levelname)-7s:%(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
logger.debug('Using SEARCH_PATH: %s', SEARCH_PATH)
logger.debug('Using EXCLUDE_PATH: %s', EXCLUDE_PATH)


class Project:
    _project_cache = None

    def __init__(self, compose_file):
        self.compose_file = compose_file

    def __repr__(self):
        return f'<{self.name}|{self.dir}>'

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self.dir.name

    @property
    def dir(self):
        return self.compose_file.parent

    def ps(self):
        os.system(f'cd {self.dir} && docker-compose ps')

    def run_command(self, args):
        click.echo(f'Using project {self.name} in {self.dir}')
        os.system(f'docker-compose --project-directory {self.dir} {" ".join(args)}')

    @staticmethod
    def from_dir(dir):
        return Project(Path(dir) / 'docker-compose.yml')

    @staticmethod
    def _all():
        matches = list()
        for search_dir in SEARCH_PATH:
            matches += pathlib.Path(search_dir).glob("**/docker-compose.yml")

        projects = list()
        for found_compose in matches:
            p = Project(found_compose)
            for ex_path in EXCLUDE_PATH:
                if p.name in ['ls', 'edit']:
                    logger.warning('Project name %s clashes with doca command line command', p)
                    break
                if str(p.dir).startswith(str(ex_path)+'/'):
                    logger.info('Skipping %s because it is ignored by %s', p, ex_path)
                    break
            else:
                if p in projects:
                    logger.info('Skipping %s because project name already found earlier', found_compose)
                else:
                    projects.append(p)
                    logger.debug('Found projects %s', p)
        return projects

    @staticmethod
    def all():
        if Project._project_cache is not None:
            return Project._project_cache
        Project._project_cache = Project._all()
        return Project._project_cache

    @staticmethod
    def find_project(x):
        pnames = [i.dir for i in Project.all()]
        result, ratio = process.extractOne(x, pnames)
        logger.debug('Fuzzysearch for %s found %s with ratio %s', x, result, ratio)
        return Project.from_dir(result)


@click.group()
def doca_cli():
    pass


@doca_cli.command('ls', help='List all projects')
def ls():
    for i in Project.all():
        click.echo(f'{i.name} {i.dir}')


@doca_cli.command('edit', help=f'Run editor on the docker-compose.yml')
@click.argument('project')
def edit(project):
    p = Project.find_project(project)
    os.system(f'{EDITOR} {p.compose_file}')


@doca_cli.command('<project>', help=f'Run a docker-compose command for <project>')
@click.argument('project')
def _dummy_command_entry(project):
    click.echo('How do we get here?')


def main():
    if len(sys.argv) > 1 and sys.argv[1] not in ['edit', 'ls']:
        project_name = sys.argv[0]
        project = Project.find_project(project_name)
        project.run_command(sys.argv[2:])
        return
    doca_cli()
