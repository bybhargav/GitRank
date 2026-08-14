from pathlib import Path
import zlib

# ----- PACK FILES -----

def find_pack_files(git_path: Path) -> tuple[list[Path], list[Path]]:
    """Returns list of idx files and pack files """
    idx_files = []
    pack_files = []

    pack_path = git_path / "objects" / "pack"

    for file in pack_path.iterdir():
        if file.suffix == ".idx":
            idx_files.append(file)

        elif file.suffix == ".pack":
            pack_files.append(file)

    return idx_files, pack_files


def read_index_file(idx_path: Path) -> bytes:
    """Read a Git pack index file."""

    with open(idx_path, "rb") as file:
        return file.read()


def read_pack_object_header(file) -> tuple[int, int]:
    first_byte = file.read(1)[0]

    object_type = (first_byte >> 4) & 0b0111

    object_size = first_byte & 0b00001111
    shift = 4

    while first_byte & 0b10000000:
        first_byte = file.read(1)[0]

        object_size |= (
            (first_byte & 0b01111111)
            << shift
        )

        shift += 7

    return object_type, object_size


def find_object_offset(
    idx_file: Path,
    object_hash: str,
) -> int | None:

    index_data = read_index_file(idx_file)

    fanout = []

    start = 8
    end = start + (256 * 4)

    for offset in range(start, end, 4):
        value = int.from_bytes(
            index_data[offset:offset + 4],
            "big",
        )
        fanout.append(value)

    object_bytes = bytes.fromhex(object_hash)

    first_byte = object_bytes[0]

    start_index = (
        0
        if first_byte == 0
        else fanout[first_byte - 1]
    )

    end_index = fanout[first_byte]

    sha_table_start = 8 + (256 * 4)

    left = start_index
    right = end_index - 1

    while left <= right:

        middle = (left + right) // 2

        sha_offset = (
            sha_table_start
            + (middle * 20)
        )

        middle_hash = index_data[
            sha_offset:sha_offset + 20
        ]

        if middle_hash == object_bytes:

            object_count = fanout[-1]

            crc_table_start = (
                sha_table_start
                + (object_count * 20)
            )

            offset_table_start = (
                crc_table_start
                + (object_count * 4)
            )

            offset_position = (
                offset_table_start
                + (middle * 4)
            )

            raw_offset = int.from_bytes(
                index_data[
                    offset_position:offset_position + 4
                ],
                "big",
            )

            if raw_offset & 0x80000000:
                large_offset_index = raw_offset & 0x7fffffff

                large_offset_table_start = (
                    offset_table_start
                    + (object_count * 4)
                )

                large_offset_position = (
                    large_offset_table_start
                    + (large_offset_index * 8)
                )

                pack_offset = int.from_bytes(
                    index_data[
                        large_offset_position:
                        large_offset_position + 8
                    ],
                    "big",
                )

            else:
                pack_offset = raw_offset

            

            return pack_offset

        if middle_hash < object_bytes:
            left = middle + 1
        else:
            right = middle - 1

    return None


def find_object_in_path(
    idx_files: list[Path],
    pack_files: list[Path],
    object_hash: str) -> tuple[Path, Path, int]:

    for idx_file in idx_files:

        offset = find_object_offset(
            idx_file,
            object_hash,
        )

        if offset is not None:
            pack_file = idx_file.with_suffix(".pack")

            return idx_file, pack_file, offset

    raise KeyError(f"Object '{object_hash}' was not found in pack indexes.")


def read_packed_object_at_offset(
    pack_file: Path,
    offset: int,
) -> tuple[str, bytes]:

    with open(pack_file, "rb") as file:
        file.seek(offset)

        object_type, object_size = read_pack_object_header(file)

        if object_type == 6:
            distance = read_ofs_delta_base(file)
            base_offset = offset - distance

            decompressor = zlib.decompressobj()
            delta_data = decompressor.decompress(
                file.read()
            )

            base_type, base_data = read_packed_object_at_offset(
                pack_file,
                base_offset,
            )

            return base_type, apply_delta(
                base_data,
                delta_data,
            )

        if object_type == 7:
            base_hash = read_ref_delta_base(file)

            decompressor = zlib.decompressobj()

            delta_data = decompressor.decompress(
                file.read()
            )

            return read_ref_delta_object(
                pack_file,
                base_hash,
                delta_data,
            )        

        object_type_map = {
            1: "commit",
            2: "tree",
            3: "blob",
            4: "tag",
        }

        object_type = object_type_map.get(object_type)

        if object_type is None:
            raise ValueError(
                "Unsupported packed object type."
            )

        decompressor = zlib.decompressobj()

        object_data = decompressor.decompress(
            file.read()
        )

        return object_type, object_data


def load_packed_object(
    git_path: Path,
    object_hash: str,
) -> tuple[str, bytes]:

    idx_files, pack_files = find_pack_files(git_path)

    idx_file, pack_file, offset = find_object_in_path(
        idx_files,
        pack_files,
        object_hash,
    )

    with open(pack_file, "rb") as file:
        file.seek(offset)

        object_type, object_size = read_pack_object_header(file)

        if object_type == 6:
            distance = read_ofs_delta_base(file)

            base_offset = offset - distance

            decompressor = zlib.decompressobj()
            delta_data = decompressor.decompress(
                file.read()
            )

            base_type, base_data = read_packed_object_at_offset(
                pack_file,
                base_offset,
            )

            object_data = apply_delta(
                base_data,
                delta_data,
            )

            return base_type, object_data

        if object_type == 7:
            base_hash = read_ref_delta_base(file)

            decompressor = zlib.decompressobj()

            delta_data = decompressor.decompress(
                file.read()
            )

            return read_ref_delta_object(
                pack_file,
                base_hash,
                delta_data,
            )

        object_type_map = {
            1: "commit",
            2: "tree",
            3: "blob",
            4: "tag",
        }

        object_type = object_type_map.get(object_type)

        if object_type is None:
            raise ValueError(
                "Unsupported packed object type."
            )

        decompressor = zlib.decompressobj()

        object_data = decompressor.decompress(
            file.read()
        )

        return object_type, object_data


def apply_delta(
    base_data: bytes,
    delta_data: bytes,
) -> bytes:
    """Apply Git delta instructions to a base object."""

    index = 0

    # Read base object size.
    base_size = 0
    shift = 0

    while True:
        byte = delta_data[index]
        index += 1

        base_size |= (byte & 0x7f) << shift

        if not byte & 0x80:
            break

        shift += 7

    # Read result object size.
    result_size = 0
    shift = 0

    while True:
        byte = delta_data[index]
        index += 1

        result_size |= (byte & 0x7f) << shift

        if not byte & 0x80:
            break

        shift += 7

    result = bytearray()

    while index < len(delta_data):
        instruction = delta_data[index]
        index += 1

        # COPY instruction.
        if instruction & 0x80:
            copy_offset = 0
            copy_size = 0

            if instruction & 0x01:
                copy_offset |= delta_data[index]
                index += 1

            if instruction & 0x02:
                copy_offset |= delta_data[index] << 8
                index += 1

            if instruction & 0x04:
                copy_offset |= delta_data[index] << 16
                index += 1

            if instruction & 0x08:
                copy_offset |= delta_data[index] << 24
                index += 1

            if instruction & 0x10:
                copy_size |= delta_data[index]
                index += 1

            if instruction & 0x20:
                copy_size |= delta_data[index] << 8
                index += 1

            if instruction & 0x40:
                copy_size |= delta_data[index] << 16
                index += 1

            if copy_size == 0:
                copy_size = 0x10000

            result.extend(
                base_data[
                    copy_offset:copy_offset + copy_size
                ]
            )

        # INSERT instruction.
        elif instruction != 0:
            insert_size = instruction & 0x7f

            result.extend(
                delta_data[
                    index:index + insert_size
                ]
            )

            index += insert_size

        else:
            raise ValueError("Invalid delta instruction.")

    if len(base_data) != base_size:
        raise ValueError("Invalid base object size.")

    if len(result) != result_size:
        raise ValueError("Invalid result object size.")

    return bytes(result)

    
def read_ofs_delta_base(file) -> int:
    byte = file.read(1)[0]

    distance = byte & 0x7f

    while byte & 0x80:
        byte = file.read(1)[0]
        distance += 1
        distance = (distance << 7) | (byte & 0x7f)

    return distance


def read_ref_delta_base(file) -> str:
    """Read the base object SHA-1 from a REF_DELTA."""

    base_hash = file.read(20)

    if len(base_hash) != 20:
        raise ValueError("Invalid REF_DELTA base hash.")

    return base_hash.hex()


def read_ref_delta_object(
    pack_file: Path,
    base_hash: str,
    delta_data: bytes,
) -> tuple[str, bytes]:
    """Resolve a REF_DELTA object."""

    pack_path = pack_file.parent
    git_path = pack_path.parent.parent.parent

    idx_files, pack_files = find_pack_files(git_path)

    _, base_pack_file, base_offset = find_object_in_path(
        idx_files,
        pack_files,
        base_hash,
    )

    base_type, base_data = read_packed_object_at_offset(
        base_pack_file,
        base_offset,
    )

    object_data = apply_delta(
        base_data,
        delta_data,
    )

    return base_type, object_data