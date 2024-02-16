import json
import os
from tempfile import NamedTemporaryFile

from click.testing import CliRunner

from topicaxisapi.cli.commands.articles import load


def test_load(app_test_session, article_data):
    runner = CliRunner()
    with NamedTemporaryFile(delete=False) as f:
        f.write(json.dumps(article_data).encode())
        f.close()
        result = runner.invoke(load, [f.name], catch_exceptions=False)

        os.unlink(f.name)
        assert result.exit_code == 0
        assert result.output == "Processed 1 lines\n"
