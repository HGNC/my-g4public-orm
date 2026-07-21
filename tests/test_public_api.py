"""Public API surface tests for ``my_g4public_orm``.

Asserts that all 17 ORM models, the generic ``Repository``, the session
module-function surface, the settings/base types, and the re-exported
``db-common`` exceptions/capabilities are importable directly from the
package root.
"""

from __future__ import annotations

import my_g4public_orm

EXPECTED_MODELS = [
    "PubHgnc",
    "FamilyNew",
    "FamilyAlias",
    "Hierarchy",
    "HierarchyClosure",
    "Cell",
    "LocusStatsChr",
    "Comment",
    "Gencc",
    "Mane",
    "RatMusSymbol",
    "HcopOrthologs",
    "ExternalResource",
    "Specialist",
    "GeneHasFamily",
    "FamilyHasExternalResource",
    "FamilyHasSpecialist",
]

EXPECTED_SESSION_SYMBOLS = [
    "initialize_engine",
    "get_engine",
    "get_settings",
    "get_readwrite_session",
    "get_readonly_session",
    "close_all_sessions",
    "refresh_engine",
]

EXPECTED_CORE_SYMBOLS = [
    "DeclarativeBase",
    "DatabaseSettings",
]

EXPECTED_EXCEPTION_SYMBOLS = [
    "DatabaseError",
    "ConfigurationError",
    "ConnectionError",
    "SessionError",
    "ReadOnlySessionError",
]

EXPECTED_CAPABILITY_SYMBOLS = [
    "health_check",
    "DatabaseDriver",
]

EXPECTED_REPOSITORY_SYMBOLS = [
    "Repository",
]

ALL_EXPECTED_SYMBOLS = (
    EXPECTED_CORE_SYMBOLS
    + EXPECTED_SESSION_SYMBOLS
    + EXPECTED_EXCEPTION_SYMBOLS
    + EXPECTED_CAPABILITY_SYMBOLS
    + EXPECTED_REPOSITORY_SYMBOLS
    + EXPECTED_MODELS
)


def test_all_expected_symbols_are_exported() -> None:
    """Every expected public symbol appears in ``__all__``."""
    missing = [s for s in ALL_EXPECTED_SYMBOLS if s not in my_g4public_orm.__all__]
    assert not missing, f"Missing symbols from __all__: {missing}"


def test_all_expected_symbols_are_importable() -> None:
    """Every expected public symbol is importable from the package root."""
    missing = [s for s in ALL_EXPECTED_SYMBOLS if not hasattr(my_g4public_orm, s)]
    assert not missing, f"Symbols not importable from my_g4public_orm: {missing}"


def test_all_exported_symbols_resolve() -> None:
    """Every name in ``__all__`` resolves to a real attribute."""
    for name in my_g4public_orm.__all__:
        assert hasattr(
            my_g4public_orm, name
        ), f"'{name}' is listed in __all__ but not importable"


def test_seventeen_models_importable() -> None:
    """Exactly the 17 curated models are importable."""
    imported = [getattr(my_g4public_orm, name) for name in EXPECTED_MODELS]
    assert len(imported) == 17


def test_repository_is_generic_class() -> None:
    """``Repository`` is exposed and is a class."""
    assert isinstance(my_g4public_orm.Repository, type)


def test_version_string() -> None:
    """``__version__`` is a non-empty string."""
    assert isinstance(my_g4public_orm.__version__, str)
    assert my_g4public_orm.__version__
