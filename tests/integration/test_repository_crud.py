"""Repository CRUD round-trip test."""

import pymysql
import pytest
from sqlalchemy import create_engine

from my_g4public_orm.models import FamilyNew, GeneHasFamily, HcopOrthologs
from my_g4public_orm.repositories.base import Repository


@pytest.mark.integration
def test_repository_crud(mysql_container) -> None:
    """Test repository CRUD operations through Repository with real MySQL database."""
    # Create connection string for pymysql
    host = mysql_container.get_container_host_ip()
    port = mysql_container.get_exposed_port(3306)
    connection_url = f"mysql+pymysql://root:test@{host}:{port}/g4public"

    # Load the schema into the MySQL container using pymysql directly
    connection = pymysql.connect(
        host=host,
        port=int(port),
        user="root",
        password="test",
        database="g4public"
    )

    try:
        # Read and execute the schema file
        with open("schema/g4public.sql") as f:
            schema_sql = f.read()

        # Execute the entire schema
        with connection.cursor() as cursor:
            # Split by delimiter and execute each statement
            statements = schema_sql.split(";")
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith("--") and not statement.startswith("/*") and "USE" not in statement:
                    try:
                        cursor.execute(statement)
                    except Exception:
                        # Some statements might fail in test context, that's acceptable for now
                        pass
            connection.commit()
    finally:
        connection.close()

    # Initialize our session system with the container's connection URL
    # For this test, we'll use SQLAlchemy directly since we need to test the Repository
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(connection_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Test CRUD operations with FamilyNew (has real PK)
    session = SessionLocal()
    try:
        # Create a repository instance
        family_repo = Repository(session, FamilyNew)

        # Create
        family = FamilyNew(
            abbreviation="TEST",
            name="Test Family",
            editor="test_user",
            status="active",
            type="Test",
            desc_label="Test label",
            desc_source="Test source",
            desc_go="Test GO terms",
            typical_gene="TEST1",
            curator_comment="Test family for CRUD operations",
            external_note="Test external note",
            pubmed_ids="12345678, 87654321",
            desc_comment="Test description"
        )
        family_repo.add(family)
        session.commit()
        session.refresh(family)

        # Verify AUTO_INCREMENT worked
        assert family.id is not None, "Family should have an ID after insert"
        family_id = family.id

        # Read
        retrieved_family = family_repo.get_by_id(family_id)
        assert retrieved_family is not None, "Should be able to retrieve family by ID"
        assert retrieved_family.abbreviation == "TEST", "Retrieved family should have correct abbreviation"

        # Update
        retrieved_family.name = "Updated Test Family"
        family_repo.save(retrieved_family)
        session.commit()

        # Verify update
        updated_family = family_repo.get_by_id(family_id)
        assert updated_family.name == "Updated Test Family", "Family name should be updated"

        # Filter/Query
        filtered_families = family_repo.filter_by(abbreviation="TEST")
        assert len(filtered_families) == 1, "Should find exactly one family with TEST abbreviation"
        assert filtered_families[0].id == family_id, "Filtered family should have correct ID"

        # Test with a junction model (GeneHasFamily)
        gene_family_repo = Repository(session, GeneHasFamily)
        gene_family = GeneHasFamily(
            hgnc_id=12345,
            family_id=family_id
        )
        gene_family_repo.add(gene_family)
        session.commit()

        # Verify junction was created
        retrieved_junction = session.query(GeneHasFamily).filter_by(
            hgnc_id=12345, family_id=family_id
        ).first()
        assert retrieved_junction is not None, "Should be able to retrieve gene-family junction"

        # Test AUTO_INCREMENT with HcopOrthologs
        hcop_repo = Repository(session, HcopOrthologs)
        hcop_entry = HcopOrthologs(
            taxon_a=9606,  # human
            taxon_b=10090, # mouse
            db_id_a="HGNC:1234",
            db_id_b="MGI:5678",
            ensembl_a="ENSG00000123456",
            ensembl_b="ENSMUSG00000654321",
            support="ortholog_one2one",
            text_link_a="http://example.com/a",
            text_link_b="http://example.com/b",
            sort_order=1,
            name_a="GENE_A",
            name_b="GeneB",
            symbol_a="GNA",
            symbol_b="GNB",
            entrez_a="12345",
            entrez_b="67890",
            chr_a="1",
            chr_b="2",
            class_a="Gene",
            class_b="Approved"
        )
        hcop_repo.add(hcop_entry)
        session.commit()
        session.refresh(hcop_entry)

        # Verify AUTO_INCREMENT worked for hcop_orthologs
        assert hcop_entry.orth_id is not None, "HcopOrthologs should have an orth_id after insert"

        # Delete (clean up)
        family_repo.delete(retrieved_family)
        session.commit()

        # Verify deletion
        deleted_family = family_repo.get_by_id(family_id)
        assert deleted_family is None, "Family should be deleted"

    finally:
        session.close()
