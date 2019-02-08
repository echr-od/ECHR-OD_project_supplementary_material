import copy
import os
import subprocess

MAP_METRIC = {
    'acc': 'Accuracy',
    'recall': 'Recall',
    'f1_weighted': 'F1-Score (weighted)',
    'precision': 'Precision',
    'balanced_acc': 'Accuracy (balanced)',
    'mcc': 'Matthew Correlation Coefficient',
    'hamming_loss': "Hamming Loss",
    'jaccard_similarity_score': "Jaccard Similarity Score",
    'zero_one_loss': 'Zero-One Loss'
}

def main():
    '''
    for file in [f for f in os.listdir('appendix/tables') if f.endswith('.tex')]:
        name = file.split('.', 1)[0]
        print(name)
        subprocess.call([
        'pdflatex', '\\documentclass[varwidth]{standalone}[2011/12/21]\\pagestyle{empty}\\begin{document}\\begin{table}\\tiny \\input{appendix/tables/'+ name +'}\\end{table}\\end{document}'
        ])
        subprocess.call(['convert', '-density', '300', '-trim', 'standalone.pdf', '-quality', '100', 'appendix/tables/{}.png'.format(name)])
    '''

    with open('multiclass.md', 'w') as file:
        content = "# Multiclass\n\n"
        content += "## Tables\n\n"
        tables = [f for f in os.listdir('appendix/tables') if f.endswith('.png') and f.startswith('multiclass')]
        for t in tables:
            name = t.split('.', 1)[0]
            metric = name.split('_', 1)[1]
            content += '![{}]({})\n\n'.format(MAP_METRIC[metric],'appendix/tables/{}'.format(t))

        content = "## Confusion Matrix\n\n"
        tables = [f for f in os.listdir('appendix/cm') if f.endswith('.png') and f.startswith('multiclass')]
        order = {}
        for t in tables:
            name = t.split('.', 1)[0]
            rest = name.split('_', 3)[-1]
            
            if rest.endswith('bag-of-words_only'):
                method = rest[::-1].split('_', 2)[-1][::-1]
                flavor = 'bag-of-words_only'
                i = 0
            elif rest.endswith('descriptive_features_only'):
                method = rest[::-1].split('_', 3)[-1][::-1]
                flavor = 'descriptive_features_only'
                i = 1
            else:
                method = rest[::-1].split('_', 4)[-1][::-1]
                flavor = 'descriptive_features_and_bag-of-words'
                i = 2
            if method not in order:
                order[method] = ['', '', '']
            order[method][i] = flavor
        
        for method, flavors in order.iteritems():
            for flavor in flavors:
                content += '![{} - {}]({})\n\n'.format(method.replace('_', ' ').title(), flavor.replace('_', ' ').title(),
                    'appendix/cm/multiclass_cm_test_{}_{}.png'.format(method, flavor))

        file.write(content)

    with open('multilabel.md', 'w') as file:
        content = "# Multilabel\n\n"
        content += "## Tables\n\n"
        tables = [f for f in os.listdir('appendix/tables') if f.endswith('.png') and f.startswith('multilabel')]
        for t in tables:
            name = t.split('.', 1)[0]
            metric = name.split('_', 1)[1]
            content += '![{}]({})\n\n'.format(MAP_METRIC[metric],'appendix/tables/{}'.format(t))

        file.write(content)

    with open('binary.md', 'w') as file:
        content = "# Binary\n\n"
        content += "## Tables\n\n"
        tables = [f for f in os.listdir('appendix/tables') if f.endswith('.png') and f.startswith('binary')]
        for t in tables:
            name = t.split('.', 1)[0]
            if 'summary' in name:
                metric = name.split('_', 1)[1][::-1].split('_', 1)[-1][::-1]
                content += '[Summary {}]({})\n\n'.format(MAP_METRIC[metric],'appendix/tables/{}'.format(t))
            elif 'best' in name:
                metric = name.split('_', 1)[1][::-1].split('_', 1)[-1][::-1]
                content += '[Best {}]({})\n\n'.format(MAP_METRIC[metric],'appendix/tables/{}'.format(t))
            else:
                metric = name.split('_', 1)[1][::-1].split('_', 2)[-1][::-1]
                article = name.split('_', 1)[1][::-1].split('_', 1)[:-1][-1]
                content += '![Article {} {}]({})\n\n'.format(article, MAP_METRIC[metric],'appendix/tables/{}'.format(t))

        content += "## Learning Curves\n\n"
        tables = [f for f in os.listdir('appendix/lc') if f.endswith('.png')]
        for t in tables:
            name = t.split('.', 1)[0]
            article = name[3:].replace('_', ' ').title()
            content += '![{}]({})\n\n'.format(article,'appendix/lc/{}'.format(t))

        file.write(content)


if __name__ == "__main__":
    main()