# tropopause
Simplify creating AWS CloudFormation templates

CloudFormation provides a vast array of options and combinations for your deployment. As a starting point, you usually just want
something simple. 

This library aims to abstract away the more complex and time consuming aspects of building cloudformation templates, in favour
of more common architectures. Although there will be a certain amount of ideology in how I choose to draw the boundaries on
'common' architectures, I will endeavour to keep it extensible; encourage plugins; and always make the underlying [troposphere](https://github.com/cloudtools/troposphere)
objects accessible.
