import importlib.metadata
packages = ['pandas', 'scikit-learn', 'matplotlib', 'fastapi', 'uvicorn', 'pydantic']
with open("requirements.txt", "w") as f:
    for package in packages:
        version = importlib.metadata.version(package)
        f.write(f"{package}=={version}\n")

        