import pandas as pd
import numpy as np
from plotnine import (
    ggplot,
    aes,
    geom_col,
    geom_path,
    geom_point,
    geom_col,
    scale_color_discrete,
    guides,
    guide_legend
)


n = 10
adf = pd.DataFrame({'x': np.arange(n),
                   'y': np.arange(n),
                   'yfit': np.arange(n) + np.tile([-.2, .2], n//2),
                   'cat': ['a', 'b']*(n//2)})
                   
              
(ggplot(adf)
 + geom_col(aes('x', 'y', fill='cat'))
 + geom_point(aes('x', y='yfit', color='cat'))
 + geom_path(aes('x', y='yfit', color='cat'))
)              
              
              
              
              
              
              