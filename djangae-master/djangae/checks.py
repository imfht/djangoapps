from django.conf import settings
from django.core.checks import register, Tags, Error


CSP_SOURCE_NAMES = [
    'CSP_DEFAULT_SRC',
    'CSP_SCRIPT_SRC',
    'CSP_IMG_SRC',
    'CSP_OBJECT_SRC',
    'CSP_MEDIA_SRC',
    'CSP_FRAME_SRC',
    'CSP_FONT_SRC',
    'CSP_STYLE_SRC',
    'CSP_CONNECT_SRC',
]


@register(Tags.security)
def check_session_csrf_enabled(app_configs=None, **kwargs):
    errors = []

    # Django 1.11 has built-in session-based CSRF tokens, so if that's enabled
    # we don't need to check for the mozilla version
    if getattr(settings, "CSRF_USE_SESSIONS", False):
        return []
    else:
        errors.append(Error(
            "CSRF_USE_SESSIONS",
            hint="Please set CSRF_USE_SESSIONS to True in your settings",
            id='djangae.E001',
        ))
    return errors


@register(Tags.security)
def check_csp_is_not_report_only(app_configs=None, **kwargs):
    errors = []
    if getattr(settings, "CSP_REPORT_ONLY", False):
        errors.append(Error(
            "CSP_REPORT_ONLY_ENABLED",
            hint="Please set 'CSP_REPORT_ONLY' to False",
            id='djangae.E002',
        ))
    return errors


@register(Tags.security, deploy=True)
def check_csp_sources_not_unsafe(app_configs=None, **kwargs):
    errors = []
    for csp_src_name in CSP_SOURCE_NAMES:
        csp_src_values = getattr(settings, csp_src_name, [])
        if "'unsafe-inline'" in csp_src_values or "'unsafe-eval'" in csp_src_values:
            errors.append(Error(
                csp_src_name + "_UNSAFE",
                hint="Please remove 'unsafe-inline'/'unsafe-eval' from your CSP policies",
                id='djangae.E1%02d' % CSP_SOURCE_NAMES.index(csp_src_name),
            ))
    return errors


@register(Tags.caches, deploy=True)
def check_cached_template_loader_used(app_configs=None, **kwargs):
    """ Ensure that the cached template loader is used for Django's template system. """
    for template in settings.TEMPLATES:
        if template['BACKEND'] != "django.template.backends.django.DjangoTemplates":
            continue
        loaders = template['OPTIONS'].get('loaders', [])
        for loader_tuple in loaders:
            if loader_tuple[0] == 'django.template.loaders.cached.Loader':
                return []
        error = Error(
            "CACHED_TEMPLATE_LOADER_NOT_USED",
            hint="Please use 'django.template.loaders.cached.Loader' for Django templates",
            id='djangae.E003',
        )
        return [error]
    return []
