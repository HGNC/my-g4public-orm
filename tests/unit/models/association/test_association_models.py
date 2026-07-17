"""Test module for association (junction) models."""

from importlib import import_module

import pytest


def _load_model(module_path: str, class_name: str):
    """Load a model class and fail with a clear message if it's missing."""
    try:
        module = import_module(module_path)
    except ModuleNotFoundError as exc:  # pragma: no cover - RED stage failure path
        pytest.fail(f"Missing model module {module_path}: {exc}")

    try:
        return getattr(module, class_name)
    except AttributeError as exc:  # pragma: no cover - RED stage failure path
        pytest.fail(f"Missing model class {class_name} in {module_path}: {exc}")


def test_gene_has_family_model_structure():
    """gene_has_family has a composite PK and expected columns."""
    gene_has_family = _load_model(
        "my_g4public_orm.models.association.gene_has_family",
        "GeneHasFamily",
    )

    assert gene_has_family.__tablename__ == "gene_has_family"

    table = gene_has_family.__table__
    assert set(table.columns.keys()) == {"hgnc_id", "family_id", "url", "custom_sort"}

    primary_key_columns = [col.name for col in table.primary_key.columns]
    assert primary_key_columns == ["hgnc_id", "family_id"]

    assert table.c.hgnc_id.type.__class__.__name__ == "Integer"
    assert table.c.family_id.type.__class__.__name__ == "Integer"
    assert table.c.url.type.__class__.__name__ == "String"
    assert table.c.url.type.length == 255
    assert table.c.custom_sort.type.__class__.__name__ == "String"
    assert table.c.custom_sort.type.length == 255


def test_family_has_external_resource_model_structure():
    """family_has_external_resource has a composite PK and expected columns."""
    family_has_external_resource = _load_model(
        "my_g4public_orm.models.association.family_has_external_resource",
        "FamilyHasExternalResource",
    )

    assert family_has_external_resource.__tablename__ == "family_has_external_resource"

    table = family_has_external_resource.__table__
    assert set(table.columns.keys()) == {"family_id", "ext_id"}

    primary_key_columns = [col.name for col in table.primary_key.columns]
    assert primary_key_columns == ["family_id", "ext_id"]

    assert table.c.family_id.type.__class__.__name__ == "Integer"
    assert table.c.ext_id.type.__class__.__name__ == "Integer"


def test_family_has_specialist_model_structure():
    """family_has_specialist has a composite PK and expected columns."""
    family_has_specialist = _load_model(
        "my_g4public_orm.models.association.family_has_specialist",
        "FamilyHasSpecialist",
    )

    assert family_has_specialist.__tablename__ == "family_has_specialist"

    table = family_has_specialist.__table__
    assert set(table.columns.keys()) == {"fam_id", "specialist_id"}

    primary_key_columns = [col.name for col in table.primary_key.columns]
    assert primary_key_columns == ["fam_id", "specialist_id"]

    assert table.c.fam_id.type.__class__.__name__ == "Integer"
    assert table.c.specialist_id.type.__class__.__name__ == "Integer"
