import tempfile
import pytest
import oci
from pgbackup import storage

@pytest.fixture
def infile():
    infile = tempfile.TemporaryFile('r+b')
    infile.write(b"Testing")
    infile.seek(0)
    return infile

# Local storage tests...

def test_storing_file_locally():
    """
    Writes content from one file-like to another
    """
    infile = tempfile.TemporaryFile('r+b')
    infile.write(b"Testing")
    infile.seek(0)

    outfile = tempfile.NamedTemporaryFile(delete=False)
    storage.local(infile, outfile)
    with open(outfile.name, 'rb') as f:
        assert f.read() == b"Testing"

def test_storing_file_on_oci(mocker, infile):
    """
    Writes content from one readable to S3
    """
    client = mocker.Mock()

    storage.oci(client,
            infile,
            "bucket",
            "file-name")

    client.upload_fileobj.assert_called_with(
            infile,
            "bucket",
            "file-name")
