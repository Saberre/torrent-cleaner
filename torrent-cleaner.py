import argparse
import os
from pathlib import Path
import shutil

import bencode


def main(path, dry=False):
    # Path to resume.dat
    resume_path = os.path.join(path, 'resume.dat')
    data = open(resume_path, 'rb').read()

    # Find ongoing .torrent files from resume.dat
    torrents = bencode.decode(data)
    ongoing = []
    for k, _ in torrents.items():
        ongoing.append(os.path.join(path, k))

    # List all .torrent files in the specified directory.
    p = Path(path).glob('*.torrent')
    trashes = {str(x) for x in p} - set(ongoing)

    # Path to the trash directory
    trash_path = os.path.join(path, 'trash')
    if not dry and not os.path.isdir(trash_path):
        os.mkdir(trash_path)

    # Move unnecessary torrent files to the trash directory.
    for x in trashes:
        print('Moving %s' % x)
        if not dry:
            shutil.move(x, trash_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Clean unnecessary torrent files by comparing resume.dat and .torrent files.'
    )
    parser.add_argument('-d', '--dry', action='store_true', help='Dry run. No actual file operation occurs.')
    parser.add_argument('path', help='Folder containing .torrent files and resume.dat.')
    args = parser.parse_args()

    main(args.path, args.dry)
