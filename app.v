module main

import os

fn main() {
  os.chdir('/home/kae/Studio/Git/karuego/project_penjadwalan')!
  _ = os.execute('uv run src/myapp/main.py')
}
