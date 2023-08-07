# -*- coding: utf-8 -*-

import json, argparse



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', default='corpus.txt')
    parser.add_argument('--outfile', default='corpus.json')
    arg = parser.parse_args()

    entry = {}
    jsondata = []
    with open(arg.infile, 'r', encoding='utf8') as file:
        for line in file:
            line = line.strip()
            if line.strip('.').isnumeric():
                if 'eng' in entry and 'zh' in entry: jsondata.append(entry)
                entry = {}
            elif 'eng' not in entry:
                entry['eng'] = line.strip()
            elif 'zh' not in entry:
                entry['zh'] = line.strip()
    
    with open(arg.outfile, 'w', encoding='utf8') as file:
        file.write(json.dumps(jsondata, indent=2, ensure_ascii=False))
    
    print('export total %d json entries' % len(jsondata))
    
