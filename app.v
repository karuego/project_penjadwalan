module main

import os

fn main() {
  println('1')
  os.chdir('/home/kae/Studio/Git/karuego/project_penjadwalan')!
  println('2')
  _ = os.execute('uv run src/myapp/main.py')
  println('3')
}
