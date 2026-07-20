"""Integration repository CRUD round-trip tests against ephemeral MySQL."""

from __future__ import annotations

from sqlalchemy.orm import Session

from my_g4public_orm.models import FamilyNew, GeneHasFamily, HcopOrthologs
from my_g4public_orm.repositories.base import Repository


def test_repository_crud_round_trip_for_family_and_junction_models(
    loaded_schema_engine,
) -> None:
    """Insert/get/update/filter/delete via Repository(session, FamilyNew)."""
    with Session(loaded_schema_engine) as session:
        family_repo: Repository[FamilyNew] = Repository(session, FamilyNew)
        junction_repo: Repository[GeneHasFamily] = Repository(session, GeneHasFamily)

        created = FamilyNew(abbreviation="T10_FAM", name="Task 10 family")
        family_repo.add(created)
        session.flush()

        assert created.id is not None
        assert isinstance(created.id, int)

        fetched = family_repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.abbreviation == "T10_FAM"

        fetched.name = "Task 10 family updated"
        family_repo.save(fetched)
        session.flush()
        session.expire_all()

        updated = family_repo.get_by_id(created.id)
        assert updated is not None
        assert updated.name == "Task 10 family updated"

        matches = family_repo.filter_by(abbreviation="T10_FAM")
        assert len(matches) == 1
        assert matches[0].id == created.id

        link = GeneHasFamily(
            hgnc_id=999_999,
            family_id=created.id,
            url="https://example.org/t10",
            custom_sort="1",
        )
        junction_repo.add(link)
        session.flush()

        found = junction_repo.filter_by(hgnc_id=999_999, family_id=created.id)
        assert len(found) == 1
        assert found[0].url == "https://example.org/t10"

        family_obj = family_repo.get_by_id(created.id)
        assert family_obj is not None
        family_repo.delete(family_obj)
        session.flush()

        assert family_repo.get_by_id(created.id) is None

        session.rollback()


def test_repository_crud_round_trip_for_hcop_autoincrement(
    loaded_schema_engine,
) -> None:
    """AUTO_INCREMENT `hcop_orthologs.orth_id` should populate after insert."""
    with Session(loaded_schema_engine) as session:
        repository: Repository[HcopOrthologs] = Repository(session, HcopOrthologs)

        created = HcopOrthologs(
            taxon_a=9606,
            taxon_b=10090,
            db_id_a="HGNC:1234",
            db_id_b="MGI:5678",
            ensembl_a="ENSG00000123456",
            ensembl_b="ENSMUSG00000654321",
            support="ortholog_one2one",
            text_link_a="https://example.org/a",
            text_link_b="https://example.org/b",
            sort_order=1,
            class_a="Gene",
            class_b="Approved",
        )
        repository.add(created)
        session.flush()

        assert created.orth_id is not None
        assert isinstance(created.orth_id, int)

        fetched = repository.get_by_id(created.orth_id)
        assert fetched is not None
        assert fetched.db_id_a == "HGNC:1234"

        repository.delete(fetched)
        session.flush()

        assert repository.get_by_id(created.orth_id) is None

        session.rollback()
