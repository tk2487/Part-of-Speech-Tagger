def pos_tagger():
    file = open("training.pos", 'r')
    lines = file.readlines()
    pos = {}
    state = {}
    beg_sig = 1
    total = 0
    
    for line in lines:
        line = line.strip()
        data = line.split('\t')        
               
        if data[0]!='':
            if beg_sig == 1:
                if 'Begin_Sent' in state:
                        if data[1] in state['Begin_Sent']:
                            state['Begin_Sent'][data[1]] += 1
                        else:
                            state['Begin_Sent'][data[1]] = 1
                else:
                    state['Begin_Sent'] = {data[1]: 1}

                beg_sig = 0

            
            elif prev in state:
                    
                if data[1] in state[prev]:
                    state[prev][data[1]] += 1
                else:
                    state[prev][data[1]] = 1
            else:
                
                state[prev] = {data[1]: 1}
                
                    
            
            if data[1] in pos:
                if data[0] in pos[data[1]]:
                    pos[data[1]][data[0]] += 1
                else:
                    pos[data[1]][data[0]] = 1
            else:
                pos[data[1]] = {data[0]: 1}
            

                
            prev = data[1]

        else:
            beg_sig = 1
            
            if prev in state:
                if 'End_Sent' in state[prev]:
                    state[prev]['End_Sent'] += 1
                else:
                    state[prev]['End_Sent'] = 1
            else:
                
                state[prev] = {'End_Sent': 1}

    for i in pos:
        for j in pos[i]:
            total += pos[i][j]
        for j in pos[i]:
            pos[i][j] /= total
        total = 0

    for i in state:
        for j in state[i]:
            total += state[i][j]
        for j in state[i]:
            state[i][j] /= total
        total = 0
    
    
    beg_sig1 = 1

    pos_list = list(pos.keys())

    f = open("result.pos", 'w')

    prev_max = 0
    prev_pos = ''
    
    file1 = open("WSJ_23.words", 'r')
    lines = file1.readlines()
    for line in lines:
        line = line.strip()
        data = line.split('\t')

        if data[0] != '':
            if beg_sig1 == 1:
                prev = calc_max(data[0], pos, state, 1, 'Begin_Sent')
                prev_max = prev[0]
                prev_pos = pos_list[prev[1]]
                beg_sig1 = 0
                f.write(data[0] + '\t' + prev_pos + '\n')
            else:
                prev = calc_max(data[0], pos, state, prev_max, prev_pos)
                prev_max = prev[0]
                prev_pos = pos_list[prev[1]]
                f.write(data[0] + '\t' + prev_pos + '\n')
        
        else:
            beg_sig1 = 1
            f.write('\n')
   
    
def calc_max(word, posd, stated, prev, prevpos):
    max_list = []
    out = []
    for key in posd:
        if (word in posd[key].keys() and key in stated[prevpos].keys()):
            max_list.append(prev*posd[key][word]*stated[prevpos][key])
        else:
            max_list.append(0)

    out.append(max(max_list))
    out.append(max_list.index(max(max_list)))
    return (out)

pos_tagger()
