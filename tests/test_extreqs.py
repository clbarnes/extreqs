from extreqs import parse_requirement_files


def test_importable():
    import extreqs

    assert extreqs.__version__


def test_complex(fixture_dir):
    fpath = fixture_dir / "requirements.txt"
    install, extras = parse_requirement_files(fpath)

    assert install == ["dep1"]
    assert extras == {
        "extra1": ["dep2"],
        "extra2": ["dep3"],
        "extra3": ["dep4", "dep5"],
        "extra4": ["dep4"],
        "extra5": ["dep4"],
    }


def test_file_context(fixture_dir):
    fpath = fixture_dir / "requirements.txt"
    install, extras = parse_requirement_files(optional=fpath)

    assert install == []
    assert extras["optional"] == ["dep1", "dep2", "dep3", "dep4", "dep5"]
