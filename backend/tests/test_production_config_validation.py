import pytest
from pydantic import ValidationError
from app.config import Settings


def test_valid_production_config_succeeds():
    settings = Settings(
        environment="production",
        jwt_secret="super-secret-random-jwt-key-with-sufficient-length-32",
        database_url="postgresql+psycopg://codementor:secret@db.render.com:5432/codementor",
        redis_url="rediss://default:password@upstash-redis.com:6379",
    )
    assert settings.is_production is True
    assert settings.jwt_secret == "super-secret-random-jwt-key-with-sufficient-length-32"
    assert "db.render.com" in settings.database_url
    assert settings.redis_url == "rediss://default:password@upstash-redis.com:6379"


def test_production_rejects_missing_redis_url():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            environment="production",
            jwt_secret="super-secret-random-jwt-key-with-sufficient-length-32",
            database_url="postgresql+psycopg://codementor:secret@db.render.com:5432/codementor",
            redis_url="",
        )
    assert "redis_url must be configured in production" in str(exc_info.value).lower()


def test_production_rejects_localhost_redis_url():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            environment="production",
            jwt_secret="super-secret-random-jwt-key-with-sufficient-length-32",
            database_url="postgresql+psycopg://codementor:secret@db.render.com:5432/codementor",
            redis_url="redis://localhost:6379/0",
        )
    assert "redis_url cannot point to localhost/loopback" in str(exc_info.value).lower()


def test_production_rejects_invalid_scheme_redis_url():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            environment="production",
            jwt_secret="super-secret-random-jwt-key-with-sufficient-length-32",
            database_url="postgresql+psycopg://codementor:secret@db.render.com:5432/codementor",
            redis_url="http://remote-redis.com:6379",
        )
    assert "scheme 'redis://' or 'rediss://'" in str(exc_info.value).lower()


def test_production_rejects_default_jwt_secret():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            environment="production",
            jwt_secret="change-me-in-production",
            database_url="postgresql+psycopg://codementor:secret@db.render.com:5432/codementor",
            redis_url="rediss://default:password@upstash-redis.com:6379",
        )
    assert "strictly prohibited" in str(exc_info.value).lower() or "requires a secure jwt_secret" in str(exc_info.value).lower()


def test_production_rejects_short_jwt_secret():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            environment="production",
            jwt_secret="short-key-123",
            database_url="postgresql+psycopg://codementor:secret@db.render.com:5432/codementor",
            redis_url="rediss://default:password@upstash-redis.com:6379",
        )
    assert "too short" in str(exc_info.value).lower()


def test_production_rejects_localhost_database_url():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            environment="production",
            jwt_secret="super-secret-random-jwt-key-with-sufficient-length-32",
            database_url="postgresql+psycopg://codementor:codementor@localhost:5432/codementor",
            redis_url="rediss://default:password@upstash-redis.com:6379",
        )
    assert "localhost/loopback" in str(exc_info.value).lower()


def test_production_rejects_loopback_ip_database_url():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            environment="production",
            jwt_secret="super-secret-random-jwt-key-with-sufficient-length-32",
            database_url="postgresql+psycopg://codementor:codementor@127.0.0.1:5432/codementor",
            redis_url="rediss://default:password@upstash-redis.com:6379",
        )
    assert "localhost/loopback" in str(exc_info.value).lower()


def test_database_url_normalization():
    s1 = Settings(database_url="postgres://user:pass@remote-host:5432/mydb")
    assert s1.database_url.startswith("postgresql+psycopg://")

    s2 = Settings(database_url="postgresql://user:pass@remote-host:5432/mydb")
    assert s2.database_url.startswith("postgresql+psycopg://")


def test_dev_environment_allows_defaults():
    s = Settings(environment="development")
    assert s.is_production is False
    assert s.jwt_secret == "change-me-in-production"
    assert "localhost" in s.database_url
    assert s.redis_url is None
