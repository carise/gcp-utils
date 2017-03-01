def GenerateConfig(context):
    """Generate configuration."""

    resources = []

    resources.append({
        'name': context.env['name'],
        'type': 'sqladmin.v1beta4.instance',
        'properties': {
            'name': context.properties['instance-name'],
            'project': context.env['project'],
            'backendType': 'SECOND_GEN',
            'databaseVersion': 'MYSQL_5_7',
            'region': context.properties['region'],
            'settings': {
                'tier': 'db-n1-standard-1',
                'backupConfiguration': {
                    'enabled': True,
                    'binaryLogEnabled': True
                },
                'activationPolicy': 'ALWAYS',
                'ipConfiguration': {
                    'ipv4Enabled': True,
                        'authorizedNetworks': [
                    ],
                    'requireSsl': True
                },
                'dataDiskSizeGb': '25',
                'dataDiskType': 'PD_SSD',
            },
            'instanceType': 'CLOUD_SQL_INSTANCE',
        }
    })

    return {'resources': resources}
