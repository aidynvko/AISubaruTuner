from pathlib import Path

from .rom_integration import KNOWN_ROM_ID_OFFSETS, ROMIntegrationManager
from .xml_definition_parser import XMLDefinitionParser


def test_merpmod_definition_parses():
    definition_path = (
        Path(__file__).resolve().parent
        / "definitions"
        / "merpmod"
        / "A8DK100F.xml"
    )
    parser = XMLDefinitionParser()
    definition = parser.parse_definition_file(str(definition_path))

    assert "A8DK100F" in definition["roms"]
    assert definition["table_count"] > 0
    assert "Target Boost" in definition["tables"]


def test_merpmod_definition_auto_resolves_from_rom_id(tmp_path):
    source_rom = (
        Path(__file__).resolve().parents[1]
        / "test_files"
        / "test 192kb 4 Golden MAF Rom 2 EJ205-91OCT-EBCS-CATLESS-StockIntake.bin"
    )
    patched_rom = tmp_path / "A8DK100F_Original.bin"
    data = bytearray(source_rom.read_bytes())
    id_offset = KNOWN_ROM_ID_OFFSETS[0]
    data[id_offset : id_offset + 8] = b"A8DK100F"
    patched_rom.write_bytes(data)

    manager = ROMIntegrationManager()
    tables = manager.extract_raw_tables(str(patched_rom))

    assert isinstance(tables, dict)
    assert len(tables) > 0
    assert "Engine Load Limit (Maximum)" in tables
