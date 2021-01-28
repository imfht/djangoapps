import ast
import csv
import functools
import inspect
import json

from itertools import chain

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse, resolve

from djangae.contrib.security.commands_utils import (
    extract_views_from_urlpatterns,
    display_as_table,
    get_func_name,
    get_decorators,
    get_mixins,
    simplify_regex,
)


DEFAULT_IGNORED_MODULES = ['django', '__builtin__']


class Command(BaseCommand):
    args = "<module_to_ignore> <module_to_ignore> ..."
    help = "Displays all of the url matching routes for the project."

    def add_arguments(self, parser):
        parser.add_argument('--show_allowed_methods', action='store_true')
        parser.add_argument('--show_class_parents', action='store_true')
        parser.add_argument(
            '--output_file_type',
            nargs='?',
            choices=['json', 'csv'],
        )

    def handle(self, *args, **options):
        show_class_parents = options.get('show_class_parents')
        show_allowed_methods = options.get('show_allowed_methods')
        output_type = options.get('output_file_type')

        ignored_modules = args if args else DEFAULT_IGNORED_MODULES
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        view_functions = extract_views_from_urlpatterns(urlconf.urlpatterns, ignored_modules=ignored_modules)

        views = []
        for (func, regex, url_name) in view_functions:

            # Extract real function from partial
            if isinstance(func, functools.partial):
                func = func.func

            decorators_and_mixins = get_decorators(func) + get_mixins(func, ignored_modules=ignored_modules)

            view_info = dict(
                module='{0}.{1}'.format(func.__module__, get_func_name(func)),
                url=simplify_regex(regex),
                decorators=', '.join(decorators_and_mixins),
                parents='',
                allowed_http_methods='',
            )

            cbv_info = get_cbv_info(url_name)
            if cbv_info:
                view_info['parents'] = ', '.join(cbv_info['parent_class_names'])
                view_info['allowed_http_methods'] = ', '.join(cbv_info['allowed_http_methods'])
                view_info['decorators'] = ', '.join([
                    '{}: {}'.format(method_name, ', '.join(['@' + d for d in decorators]))
                    for method_name, decorators in cbv_info['decorators'].items()
                ])

            views.append(view_info)

        info = (
            "Decorators lists are not comprehensive and do not take account of other patching.\n"
        )

        headers = ['URL', 'Handler path', 'Decorators & Mixins']
        fields = ['url', 'module', 'decorators']

        if show_class_parents:
            headers += ['Parents']
            fields += ['parents']

        if show_allowed_methods:
            headers += ['Allowed Methods']
            fields += ['allowed_http_methods']

        formatted_views = []
        for view in views:
            formatted_views.append([view[field] for field in fields])

        table = display_as_table(formatted_views, headers)
        console_output = "\n{0}\n{1}".format(table, info)

        if output_type:
            console_output += _write_to_file(views, output_type)

        return console_output


def get_cbv_info(url_name):
    if url_name is None:
        return

    url = reverse(url_name)
    view = resolve(url).func
    is_class_based_view = inspect.isclass(view)

    if is_class_based_view:
        return {
            'decorators':  _get_class_decorators(view),
            'allowed_http_methods': view.http_method_names,
            'parent_class_names': [
                klass.__name__
                for klass in inspect.getmro(view)
                if klass.__name__ != 'object'
            ],
        }


def _get_class_decorators(cls):
    # from https://stackoverflow.com/a/31197273
    target = cls
    decorators = {}

    def visit_FunctionDef(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ''
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id

            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators


def _write_to_file(rows, output_type='json'):
    if output_type == 'json':
        filename = 'dumpurls.json'
        with open(filename, 'w+') as f:
            f.write(json.dumps(rows, sort_keys=True, indent=2, separators=(',', ': ')))

    elif output_type == 'csv':
        filename = 'dumpurls.csv'
        with open(filename, 'w+') as f:
            csv_writer = csv.DictWriter(
                f, delimiter=',', fieldnames={field for field in chain(*[r.keys() for r in rows])},
                dialect='excel', quotechar='"'
            )
            csv_writer.writeheader()
            csv_writer.writerows(rows)

    return '\nUrls dumped to: {}'.format(filename)
