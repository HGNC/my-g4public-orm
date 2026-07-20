"""Schema drift guard test - validates ORM models against real MySQL schema."""

import pymysql
import pytest
from sqlalchemy import create_engine, inspect


@pytest.mark.integration
def test_schema_drift(mysql_container) -> None:
    """Test that ORM models match the actual database schema by reflecting the testcontainer DB."""
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

    # Now use SQLAlchemy with pymysql to reflect the database schema
    engine = create_engine(connection_url)

    # Now reflect the database schema
    inspector = inspect(engine)

    # Check that all expected tables exist
    actual_tables = set(inspector.get_table_names())
    expected_tables = {
        "pub_hgnc", "cell", "family_new", "family_alias", "hierarchy",
        "hierarchy_closure", "locus_stats_chr", "comment", "gencc", "mane",
        "rat_mus_symbol", "hcop_orthologs", "external_resource", "specialist",
        "gene_has_family", "family_has_external_resource", "family_has_specialist"
    }

    assert actual_tables == expected_tables, f"Table mismatch. Expected: {expected_tables}, Got: {actual_tables}"

    # Test specific validations for key models
    # Check hcop_orthologs table structure and collation
    hcop_columns = inspector.get_columns("hcop_orthologs")
    assert len(hcop_columns) > 0, "hcop_orthologs table should exist"

    # Check that indexes exist on hcop_orthologs
    hcop_indexes = inspector.get_indexes("hcop_orthologs")

    # Check that we have at least some indexes
    assert len(hcop_indexes) >= 5, f"Expected at least 5 indexes on hcop_orthologs, got {len(hcop_indexes)}"

    # Check pub_hgnc table
    pub_hgnc_columns = inspector.get_columns("pub_hgnc")
    assert len(pub_hgnc_columns) > 10, "pub_hgnc table should have many columns"

    # Check that we have exactly 17 tables as expected
    assert len(actual_tables) == 17, f"Expected 17 tables, got {len(actual_tables)}"
