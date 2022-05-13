from typing import List

from Bio import SeqIO

database_file = 'cat14.fa'


class Item:
    def __init__(self, id, from_index, to_index):
        self.id = id
        self.from_index = from_index
        self.to_index = to_index


def clear_line(entire_line: str):
    entire_line = entire_line.replace('Q#1 - >', '')
    id, _, _, from_index, to_index, *_ = entire_line.split('\t')
    return Item(id, from_index, to_index)


def get_hitdata():
    print('Retrieving the hitdata.txt data...')
    items = []
    with open('hitdata.txt', 'r') as file:
        for index, line in enumerate(file):
            if index > 7:
                items.append(clear_line(line))
    print('Done...')
    return items


class Proteina:
    def __init__(self, id, sequence):
        self.id = id
        self.sequence = sequence


def get_cat_data():
    items = []
    print('Retrieving the fasta file data...')
    fasta_sequences = SeqIO.parse(open('cat14.fa'), 'fasta')
    for fasta in fasta_sequences:
        items.append(Proteina(id=fasta.id, sequence=str(fasta.seq)))

    print('Done...')
    return items


def write_on_file(proteina: Proteina):
    with open('output.fa', 'w') as file:
        file.write(f'{proteina.id}\n{proteina.sequence}')


if __name__ == '__main__':
    final_data = []

    items = get_hitdata()
    proteinas = get_cat_data()

    for index, item in enumerate(items):
        print(f'Finding the correct item from fasta file.... {index + 1}/{len(items)}')
        proteina: List[Proteina] = list(filter(lambda i: i.id == item.id, proteinas))
        if len(proteina) > 0:
            final_data.append(f'>{proteina[0].id}\n{proteina[0].sequence[int(item.from_index) - 1 : int(item.to_index) - 1]}')

    final_string = '\n'.join(final_data)
    with open('output.fa', 'w') as file:
        file.write(final_string)
