def In(rules, nonterminals, terminals):
    while True:
        try:
            a = input()
            if a == '':
                break
            a = a.split(' = ')
            if a[0] == 'nonterminals':
                b = a[1].split(', ')
                for i in range(len(b)):
                    nonterminals.append(b[i])
                    rules[b[i]] = []
            elif a[0] == 'terminals':
                b = a[1].split(', ')
                for i in range(len(b)):
                    terminals.append(b[i])
            else:
                b = a[0].split(' -> ')
                rules[b[0]].append(b[1].replace(' ', ''))
                rules[b[0]].sort()
        except EOFError:
            break

    return rules, nonterminals, terminals


def print_classes(rules, eq_classes, classes, nonterminals, empty_nonterminals):
    classes_print = eq_classes.copy()
    if empty_nonterminals != '':
        classes_print.append(empty_nonterminals)
    print(f"equivalent classes: {classes_print}")
    print()
    for str in eq_classes:
        for rule in rules[str[0]]:
            print(f"{str[0]} -> ", end='')
            for i in range(len(rule)):
                if rule[i] in nonterminals:
                    if rule[i] in empty_nonterminals:
                        print(empty_nonterminals[0], end='')
                    else:
                        print(f"{eq_classes[classes[rule[i]]][0]}", end='')
                else:
                    print(f"{rule[i]}", end='')
            print()


def split_classes(rules, classes):
    new_rules = dict()
    nonterminal_classes = dict()

    for key in rules:
        words = []
        for i in range(len(rules[key])):
            word = ''
            for j in range(len(rules[key][i])):
                if rules[key][i][j] in nonterminals:
                    word += str(classes[rules[key][i][j]])
                else:
                    word += rules[key][i][j]
            words.append(word)
        words = tuple(words)
        if words in new_rules:
            nonterminal_classes[words] += key
        else:
            nonterminal_classes[words] = key
            new_rules[words] = key

    new_rules = []
    index = 0
    for key in nonterminal_classes:
        new_rules.append(nonterminal_classes[key])
        for i in range(len(nonterminal_classes[key])):
            classes[nonterminal_classes[key][i]] = index
        index += 1

    return classes, new_rules


if __name__ == '__main__':

    input_rules = dict()
    rules = dict()
    classes = dict()
    terminals = []
    nonterminals = []
    empty_nonterminals = ''

    input_rules, nonterminals, terminals = In(input_rules, nonterminals, terminals)
    for key in input_rules:
        if len(input_rules[key]) != 0:
            rules[key] = input_rules[key]
        else:
            empty_nonterminals += key

    for key in nonterminals:
        classes[key] = '_'
    classes, new_rules = split_classes(rules, classes)

    old_size = len(new_rules)
    while True:
        classes, new_rules = split_classes(rules, classes)
        if old_size == len(new_rules):
            break
        old_size = len(new_rules)

    print_classes(rules, new_rules, classes, nonterminals, empty_nonterminals)

