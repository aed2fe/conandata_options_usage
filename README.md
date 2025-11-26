# conandata_options_usage
Short example to showcase how to use inject conan options from conandata file

## Overview

The basic idea of this repo is to give a best practice how to inject conan 
options from conandata file. Instead of defining the options in the 'options'
attribute they are defined in the conandata.yml file. Within the 'init()'
Method they should be added to the Options-object of the conan-recipe.

For a fully working example some dummy folders have been added to this repo as
well as some profiles to demonstrate how the final package would be built.
