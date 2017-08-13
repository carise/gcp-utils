def GenerateConfig(context):
    """Generate configuration."""

    resources = []

    resources.append({
        'name': context.env['name'],
        'type': 'iam.v1.serviceAccounts.key',
        'properties': {
            'parent': context.properties['parent'],
        },
    })

    return {'resources': resources}

