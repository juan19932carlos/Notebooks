from os import walk, system, path
import subprocess

for (dirpath, dirnames, filenames) in walk('./contracts'):
  files = [ path.join(dirpath, filename) for filename in filenames if filename[-3:] == 'pdf']
  for file in files:
    print(file)
    system( 'pdf2txt.py {input_file} > {output_file}'.format(
      input_file=file,
      output_file=file[:-3] + 'txt'
    ))
  