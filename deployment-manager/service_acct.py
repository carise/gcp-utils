def GenerateConfig(context):
    """Generate configuration."""

    resources = []

    resources.append({
        'name': context.env['name'],
        'type': 'iam.v1.serviceAccount',
        'properties': {
            'name': context.env['name'],
            'projectId': context.env['project'],
            'accountId': context.env['name'],
            'displayName': context.properties['displayName']
        }
    })

    return {'resources': resources}

