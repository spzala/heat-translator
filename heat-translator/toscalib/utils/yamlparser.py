import yaml

if hasattr(yaml, 'CSafeLoader'):
    yaml_loader = yaml.CSafeLoader
else:
    yaml_loader = yaml.SafeLoader


def load_yaml(path):
    with open(path) as f:
        return yaml.load(f.read(), Loader=yaml_loader)
