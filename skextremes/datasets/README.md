## Datasets

This packages datasets defines a set of packages which contain datasets useful
for demo, examples, etc... This can be seen as an equivalent of the ismev R 
package, but for python.

For more info about from the original source:

* http://www.ral.ucar.edu/~ericg/softextreme.php#ismev
* https://cran.r-project.org/web/packages/ismev/ismev.pdf
* https://cran.r-project.org/web/packages/ismev/index.html

There is also information from the paper:

* Harris, R. I. (1996) "[Gumbel re-visited - a new look at extreme value
statistics applied to wind speeds](http://www.sciencedirect.com/science/article/pii/0167610595000291)". 
Journal of Wind Engineering and
Industrial Arodynamics 59, 1-22.

For example, to access datasets engine, you should be able to do:

    from skextreme import datasets
    engine = datasets.engine()
    
`engine` will contain:

* a description (`engine.description`), 
* the available fields of the dataset (in this case `engine.fields.corrosion` 
and `engine.fields.time`) and
* a function to obtain all the fields as a numpy array (`engine.asarray()`).
