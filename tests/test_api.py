import os
import tarfile
import tempfile
import uuid

import pytest


async def test_firing_hook_random_uuid_404(client):
    async with client as c:
        response = await c.simulate_post(f"/hook/{uuid.uuid4()}")
        assert response.status_code == 404


async def test_firing_hook_200(client, user_999, user_999_token):
    async with client as c:
        response = await c.simulate_post(f"/hook/{user_999_token}")
        assert response.status_code == 200, response.content


async def test_backup(client, user_999, user_999_token):

    # Generate a fake tar archive
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"I am a binary file and I am gonna be tared\nEnd")
        f.seek(0)

        with tarfile.open("sample.tar", "w") as tar:
            tar.add(f.name)

        with open("sample.tar", "r") as tar:
            async with client as c:
                response = await c.simulate_post(f"/backup/db/{user_999_token}", body=tar.read())
                assert response.status_code == 200, response.content

    # Generate another fake tar archive
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"TEST-SECOND")
        f.seek(0)

        with tarfile.open("sample.tar", "w") as tar:
            tar.add(f.name)

        with open("sample.tar", "r") as tar:
            async with client as c:
                response = await c.simulate_post(f"/backup/db/{user_999_token}", body=tar.read())
                assert response.status_code == 200, response.content

    # Retrieve the tar and check it
    async with client as c:
        response = await c.simulate_get(f"/backup/db/{user_999_token}")
        assert response.status_code == 200, response.content

    with open("sample.tar", "rb") as tar:
        assert response.content == tar.read()

    os.remove("sample.tar")
