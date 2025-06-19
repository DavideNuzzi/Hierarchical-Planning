import numpy as np
from matplotlib import pyplot as plt


def plot_2x2(data, ax, box_colors, significant_combinations, significance_lines_position=None, half_line=True):

    plt.sca(ax)

    if significance_lines_position is None:
        significance_lines_position = {(0, 1): 'up', (2, 3): 'up', (0, 2): 'down', (1, 3): 'down'}

    boxplot(data, box_colors=box_colors, significance_lines_position=significance_lines_position,
            significant_combinations=significant_combinations)

    plt.xticks([1.5, 3.5], ['Structured', 'Unstructured'])
    if half_line:
        plt.axvline(2.5, -10, 10, linestyle='--', color=(0.5, 0.5, 0.5))


def plot_2x3(data, ax, box_colors, significant_combinations, significance_lines_position=None, half_line=True):

    plt.sca(ax)

    if significance_lines_position is None:
        significance_lines_position = {(0, 1): 'up', (0, 2): 'up', (1, 2): 'up', (3, 4): 'up', (4, 5): 'up', (3, 5): 'up',
                                       (0, 3): 'down', (1, 4): 'down', (2, 5): 'down'}

    boxplot(data, box_colors=box_colors, significance_lines_position=significance_lines_position,
            significant_combinations=significant_combinations)

    plt.xticks([2, 5], ['Structured', 'Unstructured'])
    if half_line:
        plt.axvline(3.5, -10, 10, linestyle='--', color=(0.5, 0.5, 0.5))


def boxplot(data, significant_combinations=[],
            sep_multiplier=1, box_colors='w', median_colors='k', boxes_alpha=1,
            linewdith=1, median_linewidth=1, significance_lines_position='up'):

    # Se i dati sono una matrice di numpy, li trasformo in una lista di array
    if type(data) is np.ndarray:
        data = [data[:, i] for i in range(data.shape[1])]

    # Converto per sicurezza tutti gli elementi delle liste in array di numpy
    data = [np.array(d) for d in data]

    # Elimino eventuali nan
    data = [d[np.isnan(d) == False] for d in data]

    # Mostro il boxplot usando la funzione di matplotlib
    bplot = plt.boxplot(data, patch_artist=True)

    # Coloro i boxplot e cambio le dimensioni delle linee
    for i, (patch, median) in enumerate(zip(bplot['boxes'], bplot['medians'])):

        if type(box_colors) is str:
            b_col = box_colors
        else:
            b_col = box_colors[i]

        if type(median_colors) is str:
            m_col = median_colors
        else:
            m_col = median_colors[i]

        patch.set_facecolor(b_col)
        median.set_color(m_col)
        patch.set_alpha(boxes_alpha)
        patch.set_linewidth(linewdith)
        median.set_linewidth(median_linewidth)

    # Plotto le differenze significative
    if len(significant_combinations) > 0:

        # print(significant_combinations)
        # Altezza iniziale per le linee
        ylim = plt.ylim()
        y_shift = 0.03 * (ylim[1] - ylim[0]) * sep_multiplier

        # Riordino le combinazioni in funzione della distanza tra i boxplot che le compongono
        box_dist = [abs(c[0] - c[1]) for c in significant_combinations]
        box_order = np.argsort(box_dist)
        significant_combinations_ordered = [significant_combinations[box_order[i]] for i in range(len(significant_combinations))]

        line_heights_up = np.array([np.max(d) for d in data])
        line_heights_down = np.array([np.min(d) for d in data])

        for i, c in enumerate(significant_combinations_ordered):
            ind1, ind2, p_value = c

            if p_value < 0.001:
                asterisks = '***'
            elif p_value < 0.01:
                asterisks = '**'
            elif p_value < 0.05:
                asterisks = '*'

            # Vedo l'altezza massima registrata di tutti i boxplot tra questi due
            # compresi essi stessi
            if significance_lines_position == 'up':
                line_pos = 'up'
            elif significance_lines_position == 'down':
                line_pos = 'down'
            elif type(significance_lines_position) is dict:
                # Cerco quella corrispondente
                if (ind1, ind2) in significance_lines_position:
                    line_pos = significance_lines_position[(ind1, ind2)]
                else:
                    line_pos = 'up'
            else:
                print('Tipo di posizionamento linee significatività non supportato')

            if line_pos == 'up':
                height = np.max(line_heights_up[ind1:(ind2+1)]) + y_shift
                tips_height = height
                line_height = tips_height + y_shift / 2
                line_heights_up[ind1:(ind2+1)] = height + y_shift * 2

            if line_pos == 'down':
                height = np.min(line_heights_down[ind1:(ind2+1)]) - y_shift
                tips_height = height
                line_height = tips_height - y_shift / 2
                line_heights_down[ind1:(ind2+1)] = height - y_shift * 2

            # Draw the significance line
            plt.plot([ind1 + 1, ind1 + 1, ind2 + 1, ind2 + 1], [tips_height, line_height, line_height, tips_height], lw=1, c='k')

            # Draw the asterisk for significance
            if line_pos == 'up':
                t_asterisk = plt.text((ind1 + ind2 + 2) * .5, line_height + y_shift * 0.3, asterisks, ha='center', va='bottom', color=[0.2, 0.2, 0.2])
            if line_pos == 'down':
                t_asterisk = plt.text((ind1 + ind2 + 2) * .5, line_height - y_shift * 0.3, asterisks, ha='center', va='top', color=[0.2, 0.2, 0.2])
