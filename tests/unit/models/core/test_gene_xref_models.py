"""Test module for the gene cross-reference models."""

from my_g4public_orm.models.core import Comment, Gencc, Mane, RatMusSymbol


def _index_names(table) -> set[str]:
    """Return the declared index names for a SQLAlchemy table."""
    return {index.name for index in table.indexes}


def test_comment_model_structure():
    """Test that the Comment model has the correct structure."""
    # Check table name
    assert Comment.__tablename__ == "comment"

    # Check table has correct columns
    table = Comment.__table__

    # Should have 2 columns: hgnc_id, note
    assert len(table.columns) == 2

    # hgnc_id column
    assert "hgnc_id" in table.columns
    assert table.c.hgnc_id.type.__class__.__name__ == "Integer"

    # note column
    assert "note" in table.columns
    assert table.c.note.type.__class__.__name__ == "Text"

    # Check composite primary key (hgnc_id, note)
    pk_columns = [col.name for col in table.primary_key.columns]
    assert set(pk_columns) == {"hgnc_id", "note"}

    # Check indexes
    assert "comment_hgnc_id_index" in _index_names(table)


def test_gencc_model_structure():
    """Test that the Gencc model has the correct structure."""
    # Check table name
    assert Gencc.__tablename__ == "gencc"

    # Check table has correct columns
    table = Gencc.__table__

    # Should have 5 columns: uuid, hgnc_id, disease_id, disease_title, omim_id
    assert len(table.columns) == 5

    # uuid column (forced ORM PK) - varchar(255)
    assert "uuid" in table.columns
    assert table.c.uuid.primary_key is True
    assert table.c.uuid.type.__class__.__name__ == "String"
    assert table.c.uuid.type.length == 255

    # hgnc_id column
    assert "hgnc_id" in table.columns
    assert table.c.hgnc_id.type.__class__.__name__ == "Integer"

    # disease_id column - varchar(255)
    assert "disease_id" in table.columns
    assert table.c.disease_id.type.__class__.__name__ == "String"
    assert table.c.disease_id.type.length == 255

    # disease_title column should be varchar(255)
    assert "disease_title" in table.columns
    assert table.c.disease_title.type.__class__.__name__ == "String"
    assert table.c.disease_title.type.length == 255

    # Check indexes
    assert "gencc_hgnc_id_index" in _index_names(table)


def test_mane_model_structure():
    """Test that the Mane model has the correct structure."""
    # Check table name
    assert Mane.__tablename__ == "mane"

    # Check table has correct columns (exactly 7)
    table = Mane.__table__
    assert len(table.columns) == 7

    # id column (real DB PK)
    assert "id" in table.columns
    assert table.c.id.primary_key is True
    assert table.c.id.type.__class__.__name__ == "Integer"

    # Check that the columns have the correct specific types and lengths from the SQL dump
    # ncbi_gene_id: int
    assert "ncbi_gene_id" in table.columns
    assert table.c.ncbi_gene_id.type.__class__.__name__ == "Integer"

    # ensembl_gene: varchar(20)
    assert "ensembl_gene" in table.columns
    assert table.c.ensembl_gene.type.__class__.__name__ == "String"
    assert table.c.ensembl_gene.type.length == 20

    # hgnc_id: int
    assert "hgnc_id" in table.columns
    assert table.c.hgnc_id.type.__class__.__name__ == "Integer"

    # refseq_nuc_acc: varchar(20)
    assert "refseq_nuc_acc" in table.columns
    assert table.c.refseq_nuc_acc.type.__class__.__name__ == "String"
    assert table.c.refseq_nuc_acc.type.length == 20

    # ensembl_nuc_acc: varchar(20)
    assert "ensembl_nuc_acc" in table.columns
    assert table.c.ensembl_nuc_acc.type.__class__.__name__ == "String"
    assert table.c.ensembl_nuc_acc.type.length == 20

    # mane_status: varchar(30)
    assert "mane_status" in table.columns
    assert table.c.mane_status.type.__class__.__name__ == "String"
    assert table.c.mane_status.type.length == 30

    # Should NOT have grch38_chr_starnd column (typo column that should be excluded)
    assert "grch38_chr_starnd" not in table.columns

    # Check indexes
    assert "mane_hgnc_id_index" in _index_names(table)


def test_rat_mus_symbol_model_structure():
    """Test that the RatMusSymbol model has the correct structure."""
    # Check table name
    assert RatMusSymbol.__tablename__ == "rat_mus_symbol"

    # Check table has correct columns
    table = RatMusSymbol.__table__

    # Should have 3 columns: rms_id, rms_sym, rms_hgnc_id
    assert len(table.columns) == 3

    # rms_id column (forced ORM PK) - varchar(25)
    assert "rms_id" in table.columns
    assert table.c.rms_id.primary_key is True
    assert table.c.rms_id.type.__class__.__name__ == "String"
    assert table.c.rms_id.type.length == 25

    # rms_sym column - varchar(25)
    assert "rms_sym" in table.columns
    assert table.c.rms_sym.type.__class__.__name__ == "String"
    assert table.c.rms_sym.type.length == 25

    # rms_hgnc_id column - int
    assert "rms_hgnc_id" in table.columns
    assert table.c.rms_hgnc_id.type.__class__.__name__ == "Integer"

    # Check indexes
    assert "rat_mus_symbol_rms_id_index" in _index_names(table)
