#!/usr/bin/env python3
import subprocess
import sys
from os.path import exists, isdir, join, basename, abspath, split, splitext
import shutil
import datetime
import re

ARTICLES_ROOT = abspath(join(split(__file__)[0], 'content', 'articles'))

def raw_markdown_to_blog_post(filename):
    whole_post = open(filename, 'r').read()
    header = '''Title: {base_filename}
Date: {today}
Slug: {base_filename}
Summary: Enter a summary for {base_filename}
'''.format(
        base_filename=splitext(basename(filename))[0],
        today=datetime.datetime.today().isoformat().split('T')[0],
    )
    whole_post = re.sub(
        r'!\[(.+)\]\((.+)\)',
        r'![\1]({attach}\2)',
        whole_post
    )
    with open(filename, 'w') as f:
        f.write(header)
        f.write(whole_post)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 nb_to_post.py NOTEBOOK_FILE")
    notebook_file = sys.argv[1]
    output_file = splitext(basename(notebook_file))[0] + '.md'
    output_path = join(ARTICLES_ROOT, output_file)
    if not exists(notebook_file):
        sys.exit("Cannot find {}".format(notebook_file))
    if exists(output_path):
        sys.exit("Remove {} to regenerate from the notebook".format(output_path))

    subprocess.check_call(['jupyter', 'nbconvert', '--to', 'markdown', notebook_file])
    shutil.move(notebook_file.replace('.ipynb', '.md'), output_path)

    nbconvert_files_dir = notebook_file.replace('.ipynb', '_files')
    if isdir(nbconvert_files_dir):
        post_files_dir = output_path.replace('.md', '_files')
        if isdir(post_files_dir):
            print("Removing/replacing {}".format(post_files_dir))
            shutil.rmtree(post_files_dir)
        shutil.move(nbconvert_files_dir, post_files_dir)
    print("Post source written to {}".format(output_path))
    raw_markdown_to_blog_post(output_path)
    print("Prepended blog post header to {}".format(output_path))