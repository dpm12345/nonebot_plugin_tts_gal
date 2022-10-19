
""" from https://github.com/keithito/tacotron """
from  .cleaners import *

def text_to_sequence(text, symbols, cleaner_names,lang):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  _symbol_to_id = {s: i for i, s in enumerate(symbols)}

  sequence = []

  clean_text = _clean_text(text, cleaner_names)
  if lang == "zh-CHS":
    sequence = cleaned_text_to_sequence_zh(clean_text,_symbol_to_id)
  elif lang == "ja":
    sequence = cleaned_text_to_sequence_ja(clean_text,_symbol_to_id)
  else:
    print("不支持的语种")
  return sequence


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
  return text

def cleaned_text_to_sequence_ja(cleaned_text,_symbol_to_id):
  sequence = []
  for symbol in cleaned_text:
    if symbol not in _symbol_to_id.keys():
      continue
    symbol_id = _symbol_to_id[symbol]
    sequence += [symbol_id]
  return sequence

def cleaned_text_to_sequence_zh(cleaned_text,_symbol_to_id):
  sequence = []
  for symbol in cleaned_text.split(" "):
    if symbol in _symbol_to_id:
      sequence.append(_symbol_to_id[symbol])
    else:
      for s in symbol:
        sequence.append(_symbol_to_id[s])
    sequence.append(_symbol_to_id[" "])
  if sequence[-1] == _symbol_to_id[" "]:
    sequence = sequence[:-1]
  return sequence