#!/user/bin/env python3
# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from matplotlib_venn import venn3
# 圆形图
my_dpi = 70
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

v=venn3(subsets = (26276, 392, 316, 93, 275, 19, 35), set_labels=('WAR', 'HTTP', 'MSG'))
#plt.show()


