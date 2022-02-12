import hashlib
import os
import shutil
from pathlib import Path

def sync(reader, filesystem, source_root, dest_root):

    source_hashes = reader(source_root)
    dest_hashes = reader(dest_root)

    source_root = Path(source_root)
    dest_root = Path(dest_root)

    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
                sourcepath = source_root / filename
                destpath = dest_root / filename
                filesystem.copy(sourcepath, destpath)

        elif dest_hashes[sha] != filename:
            olddestpath = dest_root / dest_hashes[sha]
            newdestpath = dest_root / filename
            filesystem.move(olddestpath, newdestpath)

    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            filesystem.delete(dest_root/filename)
            
class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(('COPY', src, dest))

    def move(self, src, dest):
        self.append(('MOVE', src, dest))

    def delete(self, src, dest):
        self.append(('DELETE', src, dest))


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source = {"sha1": "my-file"}
    dest = {}

    filesystem = FakeFileSystem()

    reader = {"/source":source, "/dest": dest}
    sync(reader.pop, filesystem, "/source", "/dest")
    print(filesystem)


test_when_a_file_exists_in_the_source_but_not_the_destination()