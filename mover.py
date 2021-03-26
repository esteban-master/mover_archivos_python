import argparse
import shutil
from pathlib import Path
from typing import List, NamedTuple
from sys import stderr

class MiError(Exception):
  pass

class Carpeta(NamedTuple):
  dest: str
  suffixs: List

dir_fotos = Carpeta('fotos', ['.png', '.jpeg', '.jpg'])
dir_docs = Carpeta('docs', ['.pdf', '.docx', '.txt'])
dir_programacion = Carpeta('programacion', ['.js', '.py'])

def mover(file, dest , carpeta: Carpeta):
  dest = dest / carpeta.dest
  if not dest.exists():
    print(f'Creando carpeta {carpeta.dest}')
    dest.mkdir()
  move_dest = shutil.move( str(file.absolute()) , str(dest.absolute()))
  print(f'Archivo {file.name} se movio a la carpeta -> {move_dest}')


def mover_file(file: Path, dest: Path):
  if file.suffix in dir_docs.suffixs:
    mover( file, dest, dir_docs )
  elif file.suffix in dir_fotos.suffixs:
    mover( file, dest, dir_fotos )
  elif file.suffix in dir_programacion.suffixs:
    mover( file, dest, dir_programacion )
  else:
    raise MiError(f'Archivo {file.name} no se movio porque el suffix: { file.suffix }, no es soportado')

def main():
  parser = argparse.ArgumentParser(description='Ordenar carpeta', prog='orden')
  parser.add_argument('src', type=Path, help="Carpeta a ordenar")

  args = parser.parse_args()
  src = args.src

  for src_child in src.iterdir():
    if src_child.is_file():
      try:
        mover_file( src_child, src )
      except MiError as e:
        print(e, file=stderr)


if __name__ == '__main__':
  main()


