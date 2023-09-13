


def save_dat(dataframe, header='', filename_out=''):
    with open(filename_out, 'w') as f:
        f.write(f'{header}\n')
    dataframe.to_csv(filename_out, sep='\t', mode='a', index=False, header=True)

def save_log(log_name, input_line, init_file=False):
    mode = 'w' if init_file else 'a'
    with open(log_name, mode) as f:
        f.write(f'{input_line}\n')