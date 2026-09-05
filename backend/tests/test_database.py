from db.database import _normalize_database_url


def test_normalize_database_url_replaces_postgres_prefix():
    url = "postgres://postgres.abc:secret@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    expected = "postgresql://postgres.abc:secret@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    assert _normalize_database_url(url) == expected


def test_normalize_database_url_leaves_postgresql_prefix_intact():
    url = "postgresql://postgres.abc:secret@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    assert _normalize_database_url(url) == url


def test_normalize_database_url_leaves_sqlite_prefix_intact():
    url = "sqlite:///./database.db"
    assert _normalize_database_url(url) == url
