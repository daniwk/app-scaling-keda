docker_build(
    'sb-queue-receiver',
    context='.',
    dockerfile='./deploy/app/receiver.dockerfile',
    only=['./app'],
    ignore=['./app/sender.py'],
    live_update=[
        sync('./app/', '/app/app/'),
        run(
            'poetry.lock pyproject.toml ./ && pip install --upgrade pip --user',
            trigger=['./pyproject.toml']
        )
    ]
)
docker_build(
    'sb-queue-sender',
    context='.',
    dockerfile='./deploy/app/sender.dockerfile',
    only=['./app'],
    ignore=['./app/receiver.py'],
    live_update=[
        sync('./app/', '/app/app/'),
        run(
            'poetry.lock pyproject.toml ./ && pip install --upgrade pip --user',
            trigger=['./pyproject.toml']
        )
    ]
)
k8s_yaml(kustomize('deploy/app'))
k8s_resource(
    'sb-queue-receiver',
    port_forwards='8000:8000',
    labels=['receiver']
)