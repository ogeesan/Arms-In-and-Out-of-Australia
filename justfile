default:
    just --list

# run all tests
test:
    uv run pytest tests/
    uv run "scripts/download_data.py" validate-dec-data

download-dec-data:
    uv run "scripts/download_data.py" download-dec-data
    uv run "scripts/download_data.py" validate-dec-data
