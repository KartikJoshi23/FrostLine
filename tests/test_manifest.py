from pathlib import Path

from frostline import manifest


def test_build_then_verify(tmp_path: Path):
    (tmp_path / "raw").mkdir()
    (tmp_path / "raw" / "a.csv").write_text("x\n1\n2\n", encoding="utf-8")
    (tmp_path / "b.bin").write_bytes(b"\x00\x01")

    rows = manifest.scan(tmp_path)
    assert [r["path"] for r in rows] == ["b.bin", "raw/a.csv"]
    assert rows[1]["rows"] == "2"
    assert rows[1]["made_by"].startswith("download")

    m = tmp_path / "MANIFEST.csv"
    manifest.write(rows, m)
    assert manifest.verify(tmp_path, m) == []

    (tmp_path / "raw" / "a.csv").write_text("x\n1\n", encoding="utf-8")
    (tmp_path / "new.txt").write_text("hi", encoding="utf-8")
    problems = manifest.verify(tmp_path, m)
    assert "changed: raw/a.csv" in problems
    assert "not in manifest: new.txt" in problems


def test_missing_file_is_reported(tmp_path: Path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    m = tmp_path / "MANIFEST.csv"
    manifest.write(manifest.scan(tmp_path), m)
    (tmp_path / "a.txt").unlink()
    assert manifest.verify(tmp_path, m) == ["missing: a.txt"]
