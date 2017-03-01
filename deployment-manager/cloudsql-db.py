def GenerateConfig(context):
    """Generate configuration."""

    resources = []

    resources.append({
        'name': context.env['name'],
        'type': 'sqladmin.v1beta4.database',
        'properties': {
            'name': context.env['name'],
            'project': context.env['project'],
            'instance': '$(ref.cloudsql.name)'
        }
    })

    return {'resources': resources}
